__author__ = "Luka Pacar"

from collections import Counter


def get_fermat_statistics(n: int) -> str:
    """
    Returns a string with fermat-output information of the given number.
    :param n: the number to get fermat-statistics from.
    :return: number -> percentage_to_be_prime -> number_of_is_prime_results, number_of_different_results - map of all number results
    """
    c = Counter()
    for i in range(1, n):
        fermat_result = (i ** (n - 1)) % n
        c[fermat_result] += 1

    return f"{n} -> {(c[1] / (n - 1) * 100):.0f}% -> res[1]={c[1]}, len(res)={len(c)} - {list(c.items())}"


if __name__ == "__main__":
    # Aufgabe 1:
    # Berechne (in Python) für jede der Primzahlen 𝑝 = 2 bis 𝑝 = 11 und 𝑝 = 997:
    print("Aufgabe 1:")
    print(get_fermat_statistics(2))
    print(get_fermat_statistics(11))
    print(get_fermat_statistics(997))
    print()
    # Alle 3 sind primzahlen (es kommt immer zu 100% 1 raus)

    # Aufgabe 2:
    # Was passiert bei Nicht-Primzahlen?
    for n in [2, 3, 5, 7, 11, 997, 9, 15, 21, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565,
              566, 567, 568, 569, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 6601, 8911]:
        print(get_fermat_statistics(n))
