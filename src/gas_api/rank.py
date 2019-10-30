#!/usr/bin/python3
# rank.py


def rank(distance: float, price: float, mpg: float, gal_to_fill: float) -> float:
    gal = gal_to_fill + distance / mpg
    cost = gal * price
    return cost


if __name__ == "__main__":
    print(rank(14, 2, 20, 13))
