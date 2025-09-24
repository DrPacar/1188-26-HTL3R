__author__ = "Luka Pacar"

import argparse
import logging
import math
import secrets
import sys
from typing import Tuple, Literal

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

    >>> pub, priv = generate_keys(32)  # small key for testing
    >>> e, n, _ = pub
    >>> d, _, _ = priv
    >>> for x in [0, 1, 42, 123]:
    ...     c = pow(x, e, n)
    ...     y = pow(c, d, n)
    ...     assert x == y

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


def file2ints(filename, block_size: int = 4, byte_order: Literal["little", "big"] = "big"):
    """
    Read a binary file and yield integer values of its byte blocks.

    :param filename: Path to the binary file
    :param block_size: Number of bytes per integer (default 4)
    :param byte_order: Byte order: "big" or "little" (default "big")
    :yield: Integer representation of each block of bytes

    """
    with open(filename, "rb") as f:
        while True:
            block = f.read(block_size)
            if not block:
                break
            yield int.from_bytes(block, byte_order)


def save_key(filename: str, key: Tuple[int, int, int]):
    """
    Exports a key to a file.
    :param filename: the name of the output file
    :param key: The key to Export ((e|d),n,key_len)
    """
    with open(filename, "w") as f:
        f.write(" ".join(map(str, key)))


def load_key(filename: str) -> Tuple[int, ...]:
    """Load a key from a file."""
    with open(filename, "r") as f:
        parts = tuple(map(int, f.read().split()))
        return parts


def encrypt_file(input_file: str, output_file: str, key: Tuple[int, int, int]):
    """
    Encrypt a binary file with RSA.

    :param input_file: Path to plaintext file
    :param output_file: Path to ciphertext file
    :param key: Public key tuple (e, n, key_len)
    """
    e, n, key_len = key
    input_block_size = (n.bit_length() - 1) // 8
    output_block_size = (n.bit_length() // 8) + 1

    with open(output_file, "wb") as f_out:
        for m in file2ints(input_file, input_block_size, "big"):
            c = pow(m, e, n)
            c_bytes = c.to_bytes(output_block_size, byteorder="big")
            f_out.write(c_bytes)


def decrypt_file(input_file: str, output_file: str, key: Tuple[int, int, int]):
    """
    Decrypt a binary file encrypted with RSA in binary mode.

    :param input_file: Path to the ciphertext file
    :param output_file: Path to the recovered plaintext file
    :param key: Private key tuple (d, n, key_len)
    """
    d, n, key_len = key
    input_block_size = (n.bit_length() // 8) + 1
    output_block_size = (n.bit_length() - 1) // 8

    with open(output_file, "wb") as f_out:
        for c in file2ints(input_file, input_block_size, "big"):
            m = pow(c, d, n)
            print(m)
            f_out.write(m.to_bytes(20, "big"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RSA key generation, encryption, and decryption tool.")

    # Logging / verbosity
    parser.add_argument("-l", "--loglevel", default="WARNING",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Set the logging level (default: WARNING)"
                        )

    # Main mutually exclusive group
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", "--keygen", type=int, metavar="BITS", help="Generate new key pair of given length in bits")
    group.add_argument("-e", "--encrypt", metavar="FILE", help="Encrypt the given file")
    group.add_argument("-d", "--decrypt", metavar="FILE", help="Decrypt the given file")

    # Key handling
    parser.add_argument("-k", "--key", metavar="KEYFILE",
                        help="Specify key file to use (default: local private.key/public.key files)")


    # Input/output
    parser.add_argument("-i", "--input", metavar="FILE", help="Input file")
    parser.add_argument("-o", "--output", metavar="FILE", help="Output file")

    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.loglevel))

    if args.keygen:
        public, private = generate_keys(args.keygen)
        logging.info(f"Generated RSA keys of length {args.keygen}d bits")
        save_key("public.key", public)
        save_key("private.key", private)
        print("Keys saved as public.key and private.key")

    elif args.encrypt:
        keyfile = args.key if args.key else "public.key"
        key = load_key(keyfile)
        infile = args.input if args.input else args.encrypt
        outfile = args.output if args.output else infile + ".enc"
        encrypt_file(infile, outfile, key)
        print(f"Encrypted {infile} → {outfile}")

    elif args.decrypt:
        keyfile = args.key if args.key else "private.key"
        key = load_key(keyfile)
        infile = args.input if args.input else args.decrypt
        outfile = args.output if args.output else infile + ".dec"
        decrypt_file(infile, outfile, key)
        print(f"Decrypted {infile} → {outfile}")
