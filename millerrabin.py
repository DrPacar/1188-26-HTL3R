import random


def miller_rabin(n: int, k: int):
    """
    Calculates if the given number is likely to be a prime.

    :param n: n odd integer to be tested for primality. n > 3
    :param k: the number of rounds of testing to perform
    """
    d = n
    r = 0
    while d % 2 != 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randint(2, n-2)
        x = pow(a, d, n)

        if x == 1 or x == n-1:
            continue

        break_out_of_outer_loop = False
        for _ in range(r):
            x = pow(x, 2, n)
            if x == n-1:
                break_out_of_outer_loop = True
                break

        if break_out_of_outer_loop:
            continue
        return False

    return True
