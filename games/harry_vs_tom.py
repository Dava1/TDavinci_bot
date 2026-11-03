"""Harry Potter vs Tom Riddle — a Telegram mini-game.

You are Tom Riddle. In the Chamber of Secrets you command the Basilisk 🐍
to catch Harry Potter 🧙. Harry runs towards the Basilisk across a pixel
chessboard; every turn he steps one row closer and drifts randomly to a
nearby column. You must predict the column he will step into.

* Guess right  -> the Basilisk catches Harry, you win.
* First miss   -> Fawkes pecks out the Basilisk's eyes (like in the film).
                  The board goes dark; you can only *hear* Harry.
* Third miss   -> the Sorting Hat gives Harry the Sword of Gryffindor.
* Harry reaches the Basilisk's row with the sword -> he strikes, you lose.

Commands: /game starts a match, /language picks English or Russian.
Texts live in harry_vs_tom_texts.py.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import BadRequest
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from .harry_vs_tom_texts import LANG_NAMES, pick_lang, rows_word, sounds, t

# ---------------------------------------------------------------- settings --
COLS = 8                 # chessboard width
ROWS = 6                 # row 0 = Basilisk's lair, Harry starts on the last row
HARRY_MAX_STEP = 3       # Harry drifts up to N columns left/right each turn
MISSES_TO_BLIND = 1      # Fawkes arrives after this many misses
MISSES_TO_SWORD = 3      # Sorting Hat delivers the sword after this many misses
ECHO_CHANCE = 0.15       # chance the chamber echo hides the sound's direction

CB = "hp"                # callback-data prefix
GAMES_KEY = "hp_games"   # key in chat_data
LANG_KEY = "lang"        # key in user_data

LIGHT, DARK, DARKNESS = "⬜", "⬛", "⬛"
HARRY, SNAKE, STRIKE, DEAD, SWORD = "🧙", "🐍", "💥", "💀", "⚔️"
COL_LABELS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

Event = tuple[str, dict]   # (text key, format arguments) — translated at render time


class Status(Enum):
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"


@dataclass(frozen=True)
class SoundTip:
    loudness: int     # 1 faint .. 3 loud
    sound: int        # index into the sounds list
    where: str        # "left" | "right" | "ahead" | "echo"
    rows: int         # rows between Harry and the Basilisk


# -------------------------------------------------------------- game logic --
@dataclass
class Game:
    """Pure game state — no Telegram here, so it is easy to test."""

    owner_id: int = 0
    lang: str = "en"
    rng: random.Random = field(default_factory=random.Random, repr=False)
    harry_row: int = ROWS - 1
    harry_col: int = -1
    snake_col: int = COLS // 2
    last_strike: int | None = None
    misses: int = 0
    turn: int = 0
    status: Status = Status.PLAYING
    events: list[Event] = field(default_factory=lambda: [("rules", {"step": HARRY_MAX_STEP})])
    tip: SoundTip | None = None

    def __post_init__(self) -> None:
        if self.harry_col < 0:
            self.harry_col = self.rng.randrange(COLS)

    @property
    def blind(self) -> bool:
        return self.misses >= MISSES_TO_BLIND

    @property
    def armed(self) -> bool:
        return self.misses >= MISSES_TO_SWORD

    def harry_options(self) -> list[int]:
        """Columns Harry may step into next turn."""
        lo = max(0, self.harry_col - HARRY_MAX_STEP)
        hi = min(COLS - 1, self.harry_col + HARRY_MAX_STEP)
        return list(range(lo, hi + 1))

    def strike(self, col: int) -> list[Event]:
        """Basilisk strikes column `col`; Harry moves randomly. Returns story events."""
        if self.status is not Status.PLAYING:
            raise ValueError("game is over")
        if not 0 <= col < COLS:
            raise ValueError(f"column out of range: {col}")

        self.turn += 1
        self.harry_row -= 1
        self.harry_col = self.rng.choice(self.harry_options())
        self.last_strike = col
        self.snake_col = col
        self.tip = None

        if col == self.harry_col:
            self.status = Status.WON
            self.events = [("caught_1", {"col": col + 1}), ("caught_2", {})]
            return self.events

        could_see = not self.blind
        self.misses += 1
        if could_see:
            events = [("miss_seen", {"col": col + 1, "harry": self.harry_col + 1})]
        else:
            events = [("miss_blind", {"col": col + 1})]
        if self.misses == MISSES_TO_BLIND:
            events += [("fawkes", {}), ("riddle_quote", {})]
        if self.misses == MISSES_TO_SWORD:
            events.append(("hat", {}))
        if self.harry_row == 0:
            self.status = Status.LOST
            events.append(("stab", {}))
        elif self.blind:
            self.tip = self.listen()
        self.events = events
        return events

    def give_up(self) -> None:
        self.status = Status.LOST
        self.tip = None
        self.events = [("quit", {})]

    def listen(self) -> SoundTip:
        """What the blind Basilisk hears: direction + loudness relative to its head."""
        dx = self.harry_col - self.snake_col
        loudness = 3 if dx == 0 else 2 if abs(dx) <= 2 else 1
        if self.rng.random() < ECHO_CHANCE:
            where = "echo"
        else:
            where = "left" if dx < 0 else "right" if dx > 0 else "ahead"
        sound = self.rng.randrange(len(sounds(self.lang)))
        return SoundTip(loudness, sound, where, self.harry_row)

    # ------------------------------------------------------------ rendering --
    def cell(self, r: int, c: int) -> str:
        over = self.status is not Status.PLAYING
        if self.blind and not over:
            return DARKNESS                       # the Basilisk has lost its eyes
        if (r, c) == (self.harry_row, self.harry_col):
            return {Status.WON: DEAD, Status.LOST: SWORD}.get(self.status, HARRY)
        if r == 0 and c == self.snake_col:
            return DEAD if self.status is Status.LOST else SNAKE
        if r == self.harry_row and c == self.last_strike:
            return STRIKE
        return LIGHT if (r + c) % 2 == 0 else DARK

    def board(self) -> str:
        lines = ["".join(COL_LABELS[:COLS])]
        lines += ["".join(self.cell(r, c) for c in range(COLS)) for r in range(ROWS)]
        return "\n".join(lines)

    def render(self) -> str:
        lang = self.lang
        parts = [t(lang, "title"), "", self.board(), "", t(
            lang, "status",
            eyes=t(lang, "eyes_blind" if self.blind else "eyes_seeing"),
            harry=t(lang, "harry_armed" if self.armed else "harry_unarmed"),
            turn=self.turn, misses=self.misses,
        )]
        if self.events:
            parts += ["", *(t(lang, key, **kw) for key, kw in self.events)]
        if self.status is Status.PLAYING:
            if self.tip:
                parts += ["", self.render_tip(self.tip)]
            parts += ["", t(lang, "prompt")]
        return "\n".join(parts)

    def render_tip(self, tip: SoundTip) -> str:
        lang = self.lang
        return t(lang, "tip",
                 loud=t(lang, f"loud_{tip.loudness}"),
                 sound=sounds(lang)[tip.sound],
                 where=t(lang, f"where_{tip.where}", cols=COLS),
                 rows=tip.rows, rows_word=rows_word(lang, tip.rows))

    def keyboard(self) -> InlineKeyboardMarkup:
        lang = self.lang
        if self.status is not Status.PLAYING:
            return InlineKeyboardMarkup([[InlineKeyboardButton(t(lang, "btn_again"), callback_data=f"{CB}:new")]])
        cols = [InlineKeyboardButton(str(c + 1), callback_data=f"{CB}:col:{c}") for c in range(COLS)]
        other = next(code for code in LANG_NAMES if code != lang)
        return InlineKeyboardMarkup([cols, [
            InlineKeyboardButton(t(lang, "btn_quit"), callback_data=f"{CB}:quit"),
            InlineKeyboardButton(f"🌐 {LANG_NAMES[other]}", callback_data=f"{CB}:lang:{other}"),
        ]])


# -------------------------------------------------------------- telegram UI --
def user_lang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Saved language, or a guess from the user's Telegram app language."""
    if LANG_KEY not in context.user_data:
        context.user_data[LANG_KEY] = pick_lang(getattr(update.effective_user, "language_code", None))
    return context.user_data[LANG_KEY]


def _games(context: ContextTypes.DEFAULT_TYPE) -> dict[int, Game]:
    return context.chat_data.setdefault(GAMES_KEY, {})


async def game_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/game — start a new match."""
    game = Game(owner_id=update.effective_user.id, lang=user_lang(update, context))
    msg = await update.effective_message.reply_text(game.render(), parse_mode="HTML",
                                                    reply_markup=game.keyboard())
    _games(context)[msg.message_id] = game


def _lang_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton(name, callback_data=f"{CB}:setlang:{code}")
                                  for code, name in LANG_NAMES.items()]])


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/language — choose English or Russian."""
    await update.effective_message.reply_text(t(user_lang(update, context), "lang_prompt"),
                                              reply_markup=_lang_menu())


async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    msg_id = query.message.message_id
    games = _games(context)
    _, action, *rest = query.data.split(":")
    lang = user_lang(update, context)

    if action == "setlang":                               # from the /language menu
        context.user_data[LANG_KEY] = lang = pick_lang(rest[0])
        await query.answer(LANG_NAMES[lang])
        await _edit(query, t(lang, "lang_set"), None)
        return

    if action == "new":
        game = Game(owner_id=query.from_user.id, lang=lang)
        games[msg_id] = game
        await query.answer(t(lang, "ans_new"))
        await _edit(query, game.render(), game.keyboard())
        return

    game = games.get(msg_id)
    if game is None or game.status is not Status.PLAYING:
        await query.answer(t(lang, "ans_over"), show_alert=True)
        return
    if query.from_user.id != game.owner_id:
        await query.answer(t(lang, "ans_not_owner"), show_alert=True)
        return

    if action == "lang":                                  # 🌐 button inside a game
        game.lang = context.user_data[LANG_KEY] = pick_lang(rest[0])
        await query.answer(LANG_NAMES[game.lang])
    elif action == "quit":
        game.give_up()
        await query.answer(t(game.lang, "ans_quit"))
    else:
        game.strike(int(rest[0]))
        key = {Status.WON: "ans_won", Status.LOST: "ans_lost"}.get(game.status, "ans_miss")
        await query.answer(t(game.lang, key))

    if game.status is not Status.PLAYING:
        games.pop(msg_id, None)
    await _edit(query, game.render(), game.keyboard())


async def _edit(query, text: str, markup: InlineKeyboardMarkup | None) -> None:
    try:
        await query.edit_message_text(text, parse_mode="HTML", reply_markup=markup)
    except BadRequest as exc:  # e.g. "message is not modified" on a double tap
        if "not modified" not in str(exc).lower():
            raise


def start_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Localized greeting for the bot's /start command."""
    return t(user_lang(update, context), "start")


def register(app: Application) -> None:
    """Attach the game's handlers to the bot."""
    app.add_handler(CommandHandler("game", game_command))
    app.add_handler(CommandHandler(["language", "lang"], language_command))
    app.add_handler(CallbackQueryHandler(on_button, pattern=rf"^{CB}:"))
