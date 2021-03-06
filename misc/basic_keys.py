import string

from talon.voice import Context, press

from ..utils import insert

alpha_alt = (
    "air bat cap drum each fine gust harp sit jury crunch look made near "
    + "odd pit quench red sun trap urge vest whale plex yank zip"
).split()

f_keys = {f"F {i}": f"f{i}" for i in range(1, 13)}
# arrows are separated because 'up' has a high false positive rate
arrows = ["left", "right", "up", "down", "pageup", "pagedown"]
simple_keys = ["tab", "escape", "enter", "space", "home", "pageup", "pagedown", "end"]
alternate_keys = {"delete": "backspace", "forward delete": "delete"}
symbols = {
    "back tick": "`",
    "comma": ",",
    "dot": ".",
    "point": ".",
    "period": ".",
    "semi": ";",
    "semicolon": ";",
    "tick": "'",
    "quote": '"',
    "L square": "[",
    "left square": "[",
    "square": "[",
    "R square": "]",
    "right square": "]",
    "forward slash": "/",
    "slash": "/",
    "backslash": "\\",
    "minus": "-",
    "dash": "-",
    "equals": "=",
}
modifiers = {
    "command": "cmd",
    "control": "ctrl",
    "shift": "shift",
    "alt": "alt",
    "option": "alt",
}

alphabet = dict(zip(alpha_alt, string.ascii_lowercase))
alphabet["kush"] = "k"
alphabet["nor"] = "n"
alphabet["oil"] = "o"
alphabet["yes"] = "y"
digits = {str(i): str(i) for i in range(10)}
simple_keys = {k: k for k in simple_keys}
arrows = {k: k for k in arrows}
keys = {}
keys.update(f_keys)
keys.update(simple_keys)
keys.update(alternate_keys)
keys.update(symbols)

# map alphanumeric and keys separately so engine gives priority to letter/number repeats
keymap = keys.copy()
keymap.update(arrows)
keymap.update(alphabet)
keymap.update(digits)


def get_modifiers(m):
    try:
        return [modifiers[mod] for mod in m["basic_keys.modifiers"]]
    except KeyError:
        return []


def get_keys(m):
    groups = [
        "basic_keys.keys",
        "basic_keys.arrows",
        "basic_keys.digits",
        "basic_keys.alphabet",
    ]
    for group in groups:
        try:
            return [keymap[k] for k in m[group]]
        except KeyError:
            pass
    return []


def uppercase_letters(m):
    insert("".join(get_keys(m)).upper())


def letters(m):
    insert("".join(get_keys(m)).lower())


def press_keys(m):
    mods = get_modifiers(m)
    keys_to_press = get_keys(m)
    if mods:
        press("-".join(mods + [keys_to_press[0]]))
        keys_to_press = keys_to_press[1:]
    for k in keys_to_press:
        press(k)


ctx = Context("basic_keys")
ctx.keymap(
    {
        "(uppercase | ship) {basic_keys.alphabet}+ [(lowercase | sunk)]": uppercase_letters,
        "{basic_keys.modifiers}* {basic_keys.alphabet}+": press_keys,
        "{basic_keys.modifiers}* {basic_keys.digits}+": press_keys,
        "{basic_keys.modifiers}* {basic_keys.keys}+": press_keys,
        "(go | {basic_keys.modifiers}+) {basic_keys.arrows}+": press_keys,
    }
)
ctx.set_list("alphabet", alphabet.keys())
ctx.set_list("digits", digits.keys())
ctx.set_list("keys", keys.keys())
ctx.set_list("modifiers", modifiers.keys())
ctx.set_list("arrows", arrows.keys())
