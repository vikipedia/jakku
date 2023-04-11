import typer


def text_flow(filehandle):
    for line in filehandle:
        if line.split():
            yield from line.split()
        else:
            yield ""


def lines(flow, width):
    try:
        p, n = "",""
        i = 0
        l = []
        while True:
            p, n = n, next(flow)
            if  n == "":
                yield " ".join(l) + "\n"
                l = []
                i = 0
            elif i >= width:
                yield " ".join(l)
                l = []
                i  = 0
            else:
                l.append(n)
                i = i + len(n) + 1

    except StopIteration as s:
        yield " ".join(l)
        
        
def wrap(filename:str, width:int=80):
    with open(filename) as f:
        t = text_flow(f)
        l = lines(t, width)
        for line in l:
            print(line)


if __name__ == "__main__":
    typer.run(wrap)
