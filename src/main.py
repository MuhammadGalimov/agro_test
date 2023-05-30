from decimal import Decimal
from datetime import date
from typing import Iterator
from pandas import DataFrame

from src.interest import Ruble, InterestIterator
import src.interest_table as interest_table


def main():
    deposit: dict[int, Decimal] = {
        3: Ruble(100),
        4: Ruble(0),
        5: Ruble(0),
    }

    max_withdraw: dict[int, Decimal] = {
        3: Ruble(40),
        4: Ruble(40),
        5: Ruble(40),
    }

    rate: Decimal = Decimal('0.1')

    dates: dict[int, date] = {
        3: date(2023, 1, 10),
        4: date(2023, 2, 10),
        5: date(2023, 3, 10)
    }

    interest_iter: Iterator = InterestIterator(deposit, max_withdraw, rate, dates)

    for row in interest_iter:
        print(row)

    df: DataFrame = interest_table.generate(InterestIterator(deposit, max_withdraw, rate, dates))
    print(df)


if __name__ == '__main__':
    main()
