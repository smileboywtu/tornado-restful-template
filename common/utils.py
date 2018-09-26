# -*- coding: utf-8 -*-


def decode_to_string(data):
    """

    :param data:
    :return:
    """
    decoding = {}
    for k, v in data.items():
        decoding[k] = v[0].decode() if type(v) == list and len(v) == 1 else [i.decode() for i in v]

    return decoding