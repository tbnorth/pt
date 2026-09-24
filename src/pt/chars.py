import sys

from fontTools.ttLib import TTFont

COLS = 4
WIDTH = 10
ROWS = 1000

i = 30
i = 80000

BS = 30

font = (
    "C:/Users/tbrown02/AppData/Local/Microsoft/Windows/Fonts/"
    "CaskaydiaMonoNerdFont-Regular.ttf"
)
ttfont = TTFont(font)
# print(dir(ttfont["cmap"].tables[0]))
# exit()

def green(text):
    return f"\033[32m{text}\033[0m"

def all_chars(ttfont):
    for blk, table in enumerate(ttfont["cmap"].tables):
        for codepoint, name in table.cmap.items():
            yield blk, codepoint, name
def tables():
    i = 0
    seen = set()

    for blk, codepoint, _ in all_chars(ttfont):
        if i % BS == 0:
            print(f"\n{blk:6} {codepoint:8}", end=" ")
        i += 1
        if codepoint not in seen:
            seen.add(codepoint)
            print(green(chr(codepoint)), end=" ")
        else:
            print(chr(codepoint), end=" ")

    exit()

    for _ in range(ROWS):
        for col in range(COLS):
            print(f"{i + col * WIDTH:6}", end=" ")
        for _ in range(COLS):
            for _ in range(WIDTH):
                try:
                    print(chr(i), end=" ")
                except UnicodeEncodeError:
                    print("?", end="")
                i += 1
            print("  ", end="")
        print("\n")

def list_all_chars(target):
    for blk, codepoint, name in all_chars(ttfont):
        if target not in name:
            continue
        try:
            print(f"{blk:6} {codepoint:8} {name} {chr(codepoint)} ")
        except UnicodeEncodeError:
            print(f"{blk:6} {codepoint:8} {name} ?")

if len(sys.argv) > 1:
    list_all_chars(sys.argv[1])
else:
    tables()