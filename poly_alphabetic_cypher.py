"""Module to work with classic encryption
"""
import typer


app = typer.Typer()


def get_start():
    return 97


def get_end():
    return 123


def rotate(data, n):
    return data[n:] + data[:n]


def converter(nums): return list(map(chr, nums))


phrase = "".join(converter((84, 90, 76, 68, 79, 67, 89, 81, 88, 70)))

allchars = converter(range(get_start(), get_end()))


table = {c: rotate(allchars, i) for i, c in enumerate(allchars)}


def pairs(text, phrase):
    s = len(phrase)
    if len(text) <= s:
        yield from zip(text, phrase)
    else:
        yield from zip(text[:s], phrase)
        yield from pairs(text[s:], phrase)


@app.command()
def encrypt(text: str, passphrase: str = phrase):
    text = text.lower()
    passphrase = passphrase.lower()
    breaks = [i for i, c in enumerate(text) if c == " "]
    text = text.replace(" ", "")
    textc = [table[T][ord(P)-get_start()] for T, P in pairs(text, passphrase)]
    for b in breaks:
        textc.insert(b, " ")
    message = "".join(textc)
    print(message)
    return message


@app.command()
def decrypt(cypher: str, passphrase: str = phrase):
    cypher = cypher.lower()
    passphrase = passphrase.lower()
    breaks = [i for i, c in enumerate(cypher) if c == " "]
    text = cypher.replace(" ", "")
    textc = [allchars[table[P].index(T)] for T, P in pairs(text, passphrase)]
    for b in breaks:
        textc.insert(b, " ")
    message = "".join(textc)
    print(message)
    return message


if __name__ == "__main__":
    app()
