__author__ = "Luka Pacar"


def get_fermat_statistics(n: int) -> str:
    """
    Returns a string with fermat-output information of the given number.
    :param n: the number to get fermat-statistics from.
    :return: number -> percentage_to_be_prime -> number_of_is_prime_results, number_of_different_results - map of all number results
    """
    output_map = {}
    for i in range(1, n):
        fermat_result = (i ** (n-1)) % n
        output_map[fermat_result] = output_map.get(fermat_result, 0) + 1

    return f"{n} -> {(output_map[1]/(n-1) * 100):.0f}% -> res[1]={output_map[1]}, len(res)={len(output_map)} - {list(output_map.items())}"

if __name__ == "__main__":
    print(get_fermat_statistics(556))
    pass