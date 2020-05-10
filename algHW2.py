def readFromInputfile(path):
    f = open(path, "r")
    n = f.read(1)
    m = f.read(1)
    k = f.read(1)
    for line in f:
        floorMatrix += line
    return n, m, k, floorMatrix




