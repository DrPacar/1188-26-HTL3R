__author__ = "Luka Pacar"

import math
import argparse

def fermat_factor(N):
    """
    Factor a number using Fermat's method.

    :param N: integer to factor
    :return: tuple of factors (p, q)
    """
    a = math.isqrt(N)
    if a * a < N:
        a += 1

    count = 0
    while True:
        b2 = a*a - N
        b = math.isqrt(b2)
        count += 1
        if b*b == b2:
            p = a - b
            q = a + b
            return p, q
        a += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fermat attack on RSA")
    parser.add_argument("modul", type=int, help="RSA modulus N")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    p, q = fermat_factor(args.modul)
    print(f"p -> {p}")
    print(f"q -> {q}")
