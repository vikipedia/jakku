import math


def volume(r, h):
    return math.pi*r*r*h


def volumeltr(r, h):
    """return volume in litres
    parameters:
    ----------
       r: float 
          radius in ft
       h: float
          height in ft

    returns:
    -------
      volume in litres
    """
    return cubicfttoltr(volume(r, h))


def cubicfttoltr(v):
    return 28.3168*v


def brick_length():
    return 34-35.5


def bricks(r, l):
    return 2*math.pi*r/l
