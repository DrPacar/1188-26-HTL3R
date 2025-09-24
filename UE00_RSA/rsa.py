__author__ = "Luka Pacar"

import math
import secrets
from typing import Tuple

from prime import generate_prime


def generate_e(phi: int) -> int:
    """
    Generate e for the RSA Algorithm.

    :param phi: 𝜑(𝑛) = (𝑝 − 1) ⋅ (𝑞 − 1)
    :return: Integer e - gcd(e, phi) == 1.
    """
    e = 65537  # standard e
    while math.gcd(e, phi) != 1:
        e = secrets.randbelow(phi - 2) + 2  # 2 <= e < phi
    return e


def generate_keys(number_of_bits: int) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
    """
    Generate RSA key pair.

    :param number_of_bits: Approximate key size in bits.
    :return: (public_key, private_key) tuples with e/d, n, key_len.
    """
    half = int(number_of_bits / 2)
    p, q = generate_prime(half), generate_prime(half)
    while q == p:
        q = generate_prime(half)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = generate_e(phi)
    d = pow(e, -1, phi)

    key_len = n.bit_length()
    public = (e, n, key_len)
    private = (d, n, key_len)
    return public, private
