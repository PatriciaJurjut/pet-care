import time


def current_time_milliseconds():
    return round(time.time() * 1000)


def datetime_to_timestamp(datetime_variable):
    return int(round(datetime_variable.timestamp()))
