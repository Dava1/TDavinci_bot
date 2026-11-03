"""Translations for Harry Potter vs Tom Riddle.

To add a language: copy the "en" block, translate the values, add a flag to
LANG_NAMES and a plural rule to `rows_word`. Placeholders in {braces} must stay.
"""
from __future__ import annotations

DEFAULT_LANG = "en"
LANG_NAMES = {"en": "🇬🇧 English", "ru": "🇷🇺 Русский"}

TEXTS: dict[str, dict[str, str | list[str]]] = {
    "en": {
        "title": "⚡ <b>Harry Potter vs Tom Riddle</b> 🐍",
        "rules": ("You are <b>Tom Riddle</b>. Command the Basilisk to catch Harry!\n"
                  "Each turn Harry steps one row closer and moves up to {step} columns "
                  "left or right at random. Predict the column he will step into.\n"
                  "Miss once and Fawkes blinds your snake — then you only hear him."),
        "prompt": "👇 <b>Which column will Harry step into?</b>",
        "status": "Basilisk: {eyes} │ Harry: {harry} │ Turn {turn} │ Misses {misses}",
        "eyes_seeing": "👁👁 seeing",
        "eyes_blind": "🩸🩸 blind",
        "harry_unarmed": "🧙 unarmed",
        "harry_armed": "🧙⚔️ armed",
        # story events
        "caught_1": "🐍 <i>“Kill him!”</i> The Basilisk lunges at column {col}…",
        "caught_2": "💀 <b>Harry is caught!</b> Lord Voldemort rises. You win!",
        "miss_seen": "💨 The Basilisk struck column {col}, but Harry dodged into column {harry}.",
        "miss_blind": "💨 The Basilisk struck column {col}… nothing but stone.",
        "fawkes": ("🔥 <b>Fawkes swoops down and pecks out the Basilisk's eyes!</b> "
                   "Everything goes dark — from now on you can only <b>hear</b> Harry."),
        "riddle_quote": "🗣 <i>“Kill him! The bird doesn't matter — you can still hear him!”</i>",
        "hat": "🎩 Fawkes drops the Sorting Hat… Harry pulls out the <b>Sword of Gryffindor</b>! ⚔️",
        "stab": ("⚔️ Harry reaches the Basilisk and drives the sword through its head. "
                 "<b>Tom Riddle's diary is destroyed. You lose.</b>"),
        "quit": "🏳 Tom Riddle fades away… Harry escapes with Ginny.",
        # sound tips
        "tip": "👂 {loud}: {sound}, {where}.\n📏 He is about {rows} {rows_word} away.",
        "loud_3": "🔊🔊🔊 LOUD",
        "loud_2": "🔊🔊 clear",
        "loud_1": "🔈 faint",
        "where_echo": "🌀 it echoes from every wall — the direction is impossible to tell",
        "where_left": "⬅️ from your LEFT (towards column 1)",
        "where_right": "➡️ from your RIGHT (towards column {cols})",
        "where_ahead": "⬇️ from STRAIGHT in front of you",
        "sounds": [
            "footsteps splash through a puddle",
            "robes rustle against the stone",
            "a boy is breathing hard",
            "a stone pillar is brushed by a hand",
            "a wand clatters on the floor",
        ],
        # buttons and pop-ups
        "btn_quit": "🏳 Give up",
        "btn_again": "🔄 Play again",
        "ans_new": "A new chase begins!",
        "ans_over": "This game is over. Send /game to start a new one.",
        "ans_not_owner": "Only the Heir of Slytherin who started this game can command the Basilisk.",
        "ans_quit": "You gave up.",
        "ans_won": "🐍 Caught!",
        "ans_lost": "⚔️ Defeated!",
        "ans_miss": "Missed!",
        # language menu
        "lang_prompt": "🌐 Choose your language:",
        "lang_set": "✅ Language: English. Send /game to play!",
        "start": "Hi i am TDavinci bot!\nPlay /game — Harry Potter vs Tom Riddle 🐍\n🌐 /language",
    },
    "ru": {
        "title": "⚡ <b>Гарри Поттер против Тома Реддла</b> 🐍",
        "rules": ("Ты — <b>Том Реддл</b>. Прикажи Василиску поймать Гарри!\n"
                  "Каждый ход Гарри приближается на один ряд и случайно смещается "
                  "до {step} столбцов влево или вправо. Угадай, в какой столбец он шагнёт.\n"
                  "Один промах — и Фоукс ослепит змея. Дальше ты будешь только слышать Гарри."),
        "prompt": "👇 <b>В какой столбец шагнёт Гарри?</b>",
        "status": "Василиск: {eyes} │ Гарри: {harry} │ Ход {turn} │ Промахи {misses}",
        "eyes_seeing": "👁👁 видит",
        "eyes_blind": "🩸🩸 слеп",
        "harry_unarmed": "🧙 без оружия",
        "harry_armed": "🧙⚔️ с мечом",
        "caught_1": "🐍 <i>«Убей его!»</i> Василиск бросается на столбец {col}…",
        "caught_2": "💀 <b>Гарри пойман!</b> Лорд Волан-де-Морт возрождается. Ты победил!",
        "miss_seen": "💨 Василиск ударил в столбец {col}, но Гарри увернулся в столбец {harry}.",
        "miss_blind": "💨 Василиск ударил в столбец {col}… лишь холодный камень.",
        "fawkes": ("🔥 <b>Фоукс налетает и выклёвывает Василиску глаза!</b> "
                   "Всё погружается во тьму — теперь ты можешь только <b>слышать</b> Гарри."),
        "riddle_quote": "🗣 <i>«Убей его! Птица не важна — ты всё ещё слышишь его!»</i>",
        "hat": "🎩 Фоукс роняет Распределяющую шляпу… Гарри достаёт <b>меч Гриффиндора</b>! ⚔️",
        "stab": ("⚔️ Гарри добирается до Василиска и вонзает меч ему в голову. "
                 "<b>Дневник Тома Реддла уничтожен. Ты проиграл.</b>"),
        "quit": "🏳 Том Реддл растворяется… Гарри спасается вместе с Джинни.",
        "tip": "👂 {loud}: {sound}, {where}.\n📏 До него примерно {rows} {rows_word}.",
        "loud_3": "🔊🔊🔊 ГРОМКО",
        "loud_2": "🔊🔊 отчётливо",
        "loud_1": "🔈 тихо",
        "where_echo": "🌀 эхо отражается от всех стен — направление не разобрать",
        "where_left": "⬅️ СЛЕВА от тебя (к столбцу 1)",
        "where_right": "➡️ СПРАВА от тебя (к столбцу {cols})",
        "where_ahead": "⬇️ ПРЯМО перед тобой",
        "sounds": [
            "шаги шлёпают по луже",
            "мантия шуршит о камень",
            "мальчик тяжело дышит",
            "чья-то рука касается каменной колонны",
            "палочка со стуком падает на пол",
        ],
        "btn_quit": "🏳 Сдаться",
        "btn_again": "🔄 Играть снова",
        "ans_new": "Новая погоня начинается!",
        "ans_over": "Эта игра окончена. Отправь /game, чтобы начать новую.",
        "ans_not_owner": "Командовать Василиском может только Наследник Слизерина, начавший эту игру.",
        "ans_quit": "Ты сдался.",
        "ans_won": "🐍 Пойман!",
        "ans_lost": "⚔️ Поражение!",
        "ans_miss": "Промах!",
        "lang_prompt": "🌐 Выбери язык:",
        "lang_set": "✅ Язык: русский. Отправь /game, чтобы играть!",
        "start": "Привет, я TDavinci bot!\nИграй: /game — Гарри Поттер против Тома Реддла 🐍\n🌐 /language",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    """Translated text for `key`, falling back to English."""
    text = TEXTS.get(lang, TEXTS[DEFAULT_LANG]).get(key) or TEXTS[DEFAULT_LANG][key]
    return text.format(**kwargs) if kwargs else text


def sounds(lang: str) -> list[str]:
    return TEXTS.get(lang, TEXTS[DEFAULT_LANG])["sounds"]


def rows_word(lang: str, n: int) -> str:
    if lang == "ru":
        if n % 10 == 1 and n % 100 != 11:
            return "ряд"
        if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
            return "ряда"
        return "рядов"
    return "row" if n == 1 else "rows"


def pick_lang(code: str | None) -> str:
    """Map a Telegram language_code (e.g. 'ru', 'en-US') to a supported language."""
    code = (code or "").split("-")[0].lower()
    return code if code in TEXTS else DEFAULT_LANG
