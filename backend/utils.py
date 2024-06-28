from decimal import Decimal
import string


async def pre_serialize(data: list):
    """transforms list of records to list of dicts"""
    records = [dict(record) for record in data]
    return {
        'status': 202,
        'results': records
    }


def serialize_decimal(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError("Type not serializable")


def likely_missed(word: str):
    if len(set(string.punctuation) - set(word)) < len(string.punctuation):
        return False
    return True
