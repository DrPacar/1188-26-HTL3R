__author__ = "Luka Pacar"

import random

import millerrabin


def is_prim_millerrabin(n):
    return millerrabin.miller_rabin(n, 20)


primes_100 = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
    127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
    179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
    233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
    283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
    353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
    419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
    467, 479, 487, 491, 499, 503, 509, 521, 523, 541
]


def is_prim(n):
    """
    Tests if the given number is a prime
    :param n: The number to test.
    :return: if the number is a prime. ((1/4)^20 chance to be wrong)
    """
    for prime in primes_100:
        if n % prime == 0:
            return True
    return is_prim_millerrabin(n)

def generate_prime(bits):
    """
    Generates a prime with a certain number of bits.
    :param bits: number of bits.
    :return: a prime number with the amount of given bits.
    """
    assert bits >= 2
    while True:
        candidate = random.getrandbits(bits)
        candidate |= (1 << (bits - 1)) # no 0s in front
        candidate |= 1 # uneven

        if is_prim(candidate):
            return candidate