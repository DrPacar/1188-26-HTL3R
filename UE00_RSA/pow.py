__author__ = "Luka Pacar"


def pow_iterative(a: int, b: int, n: int = None):
    """
    The Python function pow(a, b, n) can compute powers of large numbers and,
    if provided, also return the result modulo n.

    :param a: Base
    :param b: Exponent
    :param n: Modulus
    :return: Result of a**b or a**b % n if n is given
    """
    result = 1

    prev_num = a
    while b > 0:
        if b % 2 == 1:  # wenn aktuelles Bit 1 ist
            result = (result * prev_num) % n if n else result * prev_num
        prev_num = (prev_num * prev_num) % n if n else prev_num * prev_num
        b >>= 1  # nächstes Bit

    return result


if __name__ == "__main__":
    import time
    loop_times = 5000

    start_time = time.time()
    for i in range(loop_times):
        x_1 = pow_iterative(2, 10, 1000)
        x_2 = pow_iterative(11000, 12310, 23)
        x_3 = pow_iterative(312222, 1384184120, 490291)
    end_time = time.time() - start_time

    print("pow_iterative: {", x_1, x_2, x_3, "} time taken:", end_time*1000, "ms")

    start_time = time.time()
    for i in range(loop_times):
        x_1 = pow(2, 10, 1000)
        x_2 = pow(11000, 12310, 23)
        x_3 = pow(312222, 1384184120, 490291)
    end_time = time.time() - start_time

    print("pow: {", x_1, x_2, x_3, "} time taken:", end_time*1000, "ms")

