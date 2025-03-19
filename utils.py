from datetime import datetime


def str_from_timestamp(timestamp):
    date = datetime.fromtimestamp(timestamp / 1000)
    date = date.strftime("%Y-%m-%d %H:%M")
    return date


def get_today(format: str):
    today = datetime.today()
    return today.strftime(format)
