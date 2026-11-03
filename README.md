# TDavinci bot

A Telegram bot built with [python-telegram-bot](https://python-telegram-bot.org/) v22.
It includes **⚡ Harry Potter vs Tom Riddle 🐍**, a mini-game played with buttons in English 🇬🇧 or Russian 🇷🇺.

## Commands

| Command | What it does |
|---|---|
| `/start` | Greeting in the player's language |
| `/game` | Start a game of Harry Potter vs Tom Riddle |
| `/language` (or `/lang`) | Choose 🇬🇧 English or 🇷🇺 Русский |
| `/birthdays` | List of family birthdays |
| `/echo <text>` | Repeat the text back |

## The game: Harry Potter vs Tom Riddle

You play **Tom Riddle** in the Chamber of Secrets and command the **Basilisk 🐍** to catch **Harry 🧙**.

```
1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣
⬜⬛⬜⬛🐍⬛⬜⬛   ← the Basilisk's row
⬛⬜⬛⬜⬛⬜⬛⬜
⬜⬛⬜⬛⬜⬛⬜⬛
⬛⬜⬛⬜⬛⬜⬛⬜
⬜⬛⬜⬛⬜⬛⬜⬛
⬛⬜⬛🧙⬛⬜⬛⬜   ← Harry starts here
[1][2][3][4][5][6][7][8]
[🏳 Give up] [🌐 Русский]
```

**Rules**
1. Each turn, press the column (1–8) you think Harry will step into.
2. Harry moves one row closer and jumps up to **3 columns** left or right at random.
3. **Right guess:** the Basilisk catches Harry and you win 🐍.
4. **Wrong guess:** events from the film happen:
   - **1st miss:** 🔥 Fawkes pecks out the Basilisk's eyes. The whole board goes dark ⬛ and from then on you can only **hear** Harry.
   - **3rd miss:** 🎩 the Sorting Hat gives Harry the **Sword of Gryffindor** ⚔️.
   - **Harry reaches the Basilisk's row:** he strikes with the sword and you lose.

**Sound clues while blind**

```
👂 🔊🔊 clear: a boy is breathing hard, ⬅️ from your LEFT (towards column 1).
📏 He is about 4 rows away.
```

- **Loudness** shows how far Harry's column is from where the Basilisk last struck: 🔊🔊🔊 same column, 🔊🔊 1–2 columns away, 🔈 3 or more.
- **Direction:** ⬅️ left, ➡️ right, ⬇️ straight ahead.
- **Echo:** about 15% of the time 🌀 the sound echoes off the walls and the direction is hidden.

In group chats, anyone can start a game, but only the player who started it can press its buttons.

## Setup

Requires **Python 3.12+** (tested on Python 3.14 and Ubuntu 26.04).

```bash
cd ~/TDavinci_bot
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

> **Ubuntu: `ensurepip is not available`?** Either install the missing package with
> `sudo apt install python3.14-venv`, or do it without sudo:
> ```bash
> python3 -m venv --without-pip .venv
> python3 -m pip --python .venv/bin/python install pip -r requirements.txt
> ```

## Run

```bash
.venv/bin/python bot.py
```

The bot runs until you press **Ctrl + C**, and only answers while it's running.
To use it in a group, add it as a member (in @BotFather → *Bot Settings → Allow Groups?*, groups must be turned on).

**Optional:** to make the commands show in Telegram's **/** menu, send `/setcommands` to @BotFather:
```
game - Harry Potter vs Tom Riddle 🐍
language - 🌐 English / Русский
birthdays - Birthdays
```

## Project structure

```
TDavinci_bot/
├── bot.py                        # entry point: creates the bot, registers commands
├── requirements.txt              # pinned dependencies
└── games/
    ├── harry_vs_tom.py           # game rules (Game class) + Telegram handlers
    └── harry_vs_tom_texts.py     # all English / Russian texts
```

`Game` in `harry_vs_tom.py` contains no Telegram code, so you can test the game rules on their own:

```python
from games.harry_vs_tom import Game, Status
g = Game(lang="ru")
g.strike(3)
print(g.render())
```

## Configuration

Difficulty settings are at the top of `games/harry_vs_tom.py`:

| Setting | Default | Meaning |
|---|---|---|
| `COLS` | 8 | Board width (max 9) |
| `ROWS` | 6 | Board height. Harry gets `ROWS - 1` moves |
| `HARRY_MAX_STEP` | 3 | How far Harry can jump sideways each turn |
| `MISSES_TO_BLIND` | 1 | Misses before Fawkes blinds the Basilisk |
| `MISSES_TO_SWORD` | 3 | Misses before Harry gets the sword |
| `ECHO_CHANCE` | 0.15 | Chance a sound clue gives no direction |

With the defaults, guessing at random wins about 49% of the time. Using the clues well wins more often.

## Adding a language

1. In `games/harry_vs_tom_texts.py`, copy the `"en"` block and translate the values. Keep the `{placeholders}` unchanged.
2. Add the language to `LANG_NAMES`, e.g. `"de": "🇩🇪 Deutsch"`.
3. If the language has its own plural forms for "row", add a rule to `rows_word()`.

> The 🌐 button in a game switches to the first *other* language in `LANG_NAMES`. That's ideal for two languages.
> With three or more, players should use `/language`, which shows them all.

## Security

The bot token is currently written directly in `bot.py`. Anyone who sees that file can control the bot.
Get a new token from @BotFather (`/revoke`), then keep it in an environment variable instead:

```python
import os
TOKEN = os.environ["BOT_TOKEN"]
```
```bash
BOT_TOKEN=123:abc .venv/bin/python bot.py
```
