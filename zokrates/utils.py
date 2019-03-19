from bitstring import BitArray

from .eddsa import Point
from .field import FQ
import hashlib


def to_bytes(*args):
    """
    Helper function that returns byte representation for objects used in this module
    """
    result = b""
    for M in args:
        if isinstance(M, Point):
            result += to_bytes(M.x)
            # result += to_bytes(M.y)
        elif isinstance(M, FQ):
            result += to_bytes(M.n)
        elif isinstance(M, int):
            result += M.to_bytes(32, "big")
        elif isinstance(M, BitArray):
            result += M.tobytes()
        elif isinstance(M, bytes):
            result += M
        elif isinstance(M, (list, tuple)):
            result += b"".join(to_bytes(_) for _ in M)
        else:
            raise TypeError("Bad type for M: " + str(type(M)))
    return result


def pprint_for_zokrates(pk, sig, msg):

    M0 = msg.hex()[:64]
    M1 = msg.hex()[64:]

    sig_R, sig_S = sig
    for n, h in zip(["M0", "M1"], [M0, M1]):
        pprint_hex(n, h)

    pprint_point("A", pk.p)
    pprint_point("R", sig_R)
    pprint_fe("S", sig_S)


def write_for_zokrates_cli(pk, sig, msg, path):

    sig_R, sig_S = sig
    args = [sig_R.x, sig_R.y, sig_S, pk.p.x.n, pk.p.y.n]
    args = " ".join(map(str, args))

    M0 = msg.hex()[:64]
    M1 = msg.hex()[64:]
    b0 = BitArray(int(M0, 16).to_bytes(32, "big")).bin
    b1 = BitArray(int(M1, 16).to_bytes(32, "big")).bin
    args = args + " " + " ".join(b0 + b1)

    with open(path, "w+") as file:
        for l in args:
            file.write(l)


def pprint_hex(n, h):
    b = BitArray(int(h, 16).to_bytes(32, "big")).bin
    s = "[" + ", ".join(b) + "]"
    print("field[256] {} = {} \n".format(n, s))


def pprint_point(n, p):
    x, y = p
    print("field[2] {} = [{}, {}] \n".format(n, x, y))


def pprint_fe(n, fe):
    print("field {} = {} \n".format(n, fe))
