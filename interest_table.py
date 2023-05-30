from interest import InterestIterator
from datetime import date, timedelta
from calendar import monthrange
from decimal import Decimal
import pandas as pd


def generate(interest_iter: InterestIterator) -> pd.DataFrame:
    days_month = lambda dt: monthrange(dt.year, dt.month)[1]
    next_date = lambda dt: (dt.replace(day=1) + timedelta(days_month(dt))).replace(day=dt.day)
    lst: list = []
    balance: Decimal = Decimal(0)
    period: int = 0
    interest_iter = iter(interest_iter)

    while True:
        try:
            row = next(interest_iter)

            date1: date = row.date1
            deposit: Decimal = row.withdraw
            max_withdraw: Decimal = row.max_return
            rate: Decimal = row.rate
        # Если итератор закончился, но кредит еще не погашен
        except StopIteration:
            date1: date = lst[period - 1]['date2']
            deposit: Decimal = Decimal(0).quantize(Decimal('1.00'))
            max_withdraw: Decimal = lst[period - 1]['max_withdraw']
            rate: Decimal = lst[period - 1]['rate'] 

        date2: date = next_date(date1)
        amount_of_days: int = (date2 - date1).days

        # Если добавится еще сумма кредита
        balance: Decimal = deposit
        if period > 0:
            balance += lst[period - 1]['balance'] - lst[period - 1]['payment'] + lst[period - 1]['interest']

        # Если кредит выплачен, печатаем завершающую строку
        if balance <= 0:
            lst.append({
                'period': period + 1,
                'date1': date1,
                'date2': date1,
                'deposit': Decimal(0).quantize(Decimal('1.00')),
                'max_withdraw': Decimal(0).quantize(Decimal('1.00')),
                'rate': rate,
                'balance': Decimal(0).quantize(Decimal('1.00')),
                'interest': Decimal(0).quantize(Decimal('1.00')),
                'payment': Decimal(0).quantize(Decimal('1.00')),    
            })

            break

        # Вычисляем проценты, которые необходимо выплатить
        interest = (balance * rate) / Decimal(365) * amount_of_days
        
        # Всегда стараемся выплатить максимально возможную сумму, 
        # часть которой - это проценты
        if balance + interest < max_withdraw:
            payment = balance + interest
        else:
            payment = max_withdraw
        
        lst.append({
            'period': period + 1,
            'date1': date1,
            'date2': date2,
            'deposit': deposit,
            'max_withdraw': max_withdraw,
            'rate': rate,
            'balance': balance.quantize(Decimal('1.00')),
            'interest': interest.quantize(Decimal('1.00')),
            'payment': payment.quantize(Decimal('1.00')),    
        })

        period += 1

    df = pd.DataFrame(lst, columns=[
        'period', 
        'date1',
        'date2',
        'deposit',
        'max_withdraw',
        'rate',
        'balance',
        'interest',
        'payment',
        ])
    
    return df
