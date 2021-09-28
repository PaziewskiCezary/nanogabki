from contextlib import contextmanager
from datetime import timedelta, datetime


def limit_measurements(experiemnt, time_limit:timedelta=None):
    if time_limit is None:
        time_limit = timedelta.max
    measurements = iter(experiemnt)
    try:
        measurement_first = next(measurements)
    except StopIteration:
        return
    time_first_measurement = datetime.fromtimestamp(measurement_first._date)
    time_since_first_measurement = datetime.fromtimestamp(measurement_first._date) - time_first_measurement
    yield time_since_first_measurement, measurement_first
    for measurement in measurements:
        if measurement._date - measurement_first._date > time_limit.total_seconds():
            break
        time_since_first_measurement = datetime.fromtimestamp(measurement._date) - time_first_measurement
        yield time_since_first_measurement, measurement
    return

def resistance_measuerment_error(resistance):
    '''Returns resisnace measurement error for Sanwa RD700 in ohms'''
    
    str_resistance = str(resistance)
    error = 0
    power = len(str_resistance.split('.')[-1]) if '.' in str_resistance else 0
    dgt = 0.1 ** power
    resistance = float(resistance) 
    
    if resistance < 400:
        error += resistance * 0.8 / 100
        error += dgt * 6
    elif resistance < 4_000:
        error += resistance * 0.6 / 100
        error += dgt * 4
    elif resistance < 40_000:
        error += resistance * 0.6 / 100
        error += dgt * 4
    elif resistance < 400_000:
        error += resistance * 0.6 / 100
        error += dgt * 4
    elif resistance < 4_000_000:
        error += resistance * 1.0 / 100
        error += dgt * 4
    elif resistance < 40_000_000:
        error += resistance * 2.0 / 100
        error += dgt * 4
    else:
        raise ValueError(f'"resistance" of value: {resistance} is out of range')
        
    return error


if __name__ == '__main__':
    from decimal import Decimal
    a = resistance_measuerment_error(Decimal("389.000"))
    print(a)
