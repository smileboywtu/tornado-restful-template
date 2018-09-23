# -*- coding: utf-8 -*-

"""


:create: 2018/9/23
:copyright: smileboywtu

"""

import msgpack


class MSGPackSerializer():
    @classmethod
    def encode(value):
        """
        save bytes
        
        :param value: 
        :return: 
        """
        return msgpack.dumps(value, encoding="utf-8").decode("iso-8859-1").encode()

    @classmethod
    def decode(value):
        return msgpack.loads(value.decode().encode("iso-8859-1"), encoding="utf-8")
