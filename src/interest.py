from decimal import Decimal
from datetime import date
from typing import Iterator


# Функция для перевода int в Decimal
def Ruble(amount: int) -> Decimal:
    if isinstance(amount, int) and amount >= 0:
        return Decimal(str(amount) + '.00')
    
    raise TypeError


# Дескрипторы немного ограничивают изменение данных
class BaseDescriptor:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]
    
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

class DecimalInterest(BaseDescriptor):
    def __set__(self, instance, value):
        if isinstance(value, Decimal) and value >= 0:
            instance.__dict__[self.name] = value
        else:
            raise TypeError
    
class IntInterest(BaseDescriptor):
    def __set__(self, instance, value):
        if isinstance(value, int) and value >= 0:
            instance.__dict__[self.name] = value
        else:
            raise TypeError
    
class DateInterest(BaseDescriptor):
    def __set__(self, instance, value):
        if isinstance(value, date):
            instance.__dict__[self.name] = value
        else:
            raise TypeError
    

class InterestInput:
    period = IntInterest()
    date1 = DateInterest()
    date2 = DateInterest()
    withdraw = DecimalInterest()
    max_return = DecimalInterest()
    rate = DecimalInterest()

    def __init__(
            self,
            period: int,
            date1: date,
            date2: date,
            withdraw: Decimal,
            max_return: Decimal,
            rate: Decimal
            ) -> None:
        self.period: IntInterest = period
        self.date1: DateInterest = date1
        self.date2: DateInterest = date2
        self.withdraw: DecimalInterest = withdraw
        self.max_return: DecimalInterest = max_return
        self.rate: DecimalInterest = rate

    def __str__(self) -> str:
        return f'{self.period} {self.date1} {self.date2} ' \
               f'{self.withdraw} {self.max_return} {self.rate}'


class InterestIterator:
    def __init__(
            self,
            withdraw: dict[int, Decimal],
            max_return: dict[int, Decimal],
            rate: Decimal,
            dates: dict[int, date]
            ) -> None:
        # Такая структура сделана для экономии памяти, так как
        # все равно по условию задачи поля withdraw, max_return и dates приватные.
        # При необходимости, можно добавить соответствующие property 
        # для доступа к этим атрибутам. 
        self._data: list[(int, (date, Decimal, Decimal))] = list()
        self._rate: Decimal = rate

        for k in sorted(list(set(dates.keys()) & set(withdraw.keys()) & set(max_return.keys()))):
            self._data.append((k, (dates[k], withdraw[k], max_return[k])))

    def __iter__(self) -> Iterator:
        self._index: int = -1
        
        return self

    def __next__(self) -> InterestInput:
        self._index += 1

        if self._index >= len(self._data):
            raise StopIteration
        
        if self._index == len(self._data) - 1:
            next_index: int = self._index
        else:
            next_index: int = self._index + 1
        
        return InterestInput(
            self._data[self._index][0],
            self._data[self._index][1][0],
            self._data[next_index][1][0],
            self._data[self._index][1][1],
            self._data[self._index][1][2],
            self._rate
        )
