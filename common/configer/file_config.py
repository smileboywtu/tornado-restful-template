# -*- coding: utf-8 -*-

"""


use python file to config


"""
import hashlib
import json
import os
from operator import itemgetter, setitem

import yaml


class FileConfig():
    __slots__ = ["_settings", "path", "_update", "_checksum"]

    def __init__(self, file_path):

        self.path = os.path.abspath(file_path)
        self._settings = {}
        self._load_file()
        self._load_environ()
        self._update = False
        self._checksum = hashlib.md5(json.dumps(self._settings, sort_keys=True).encode("utf-8")).hexdigest()

    def _load_file(self):
        self._settings = yaml.safe_load(open(self.path).read())

    def _load_environ(self):
        """
        environment start with APP_
        :return: 
        """
        for key, value in os.environ.items():
            if key.startswith("APP_"):
                self._settings[key] = value

    def reload(self):
        self._load_file()
        self._load_environ()
        _checksum = hashlib.md5(json.dumps(self._settings, sort_keys=True).encode("utf-8")).hexdigest()
        self._update = True if self._checksum != _checksum else False
        self._checksum = _checksum

    @property
    def settings(self):
        return self._settings

    def __getitem__(self, item):
        itemgetter(item)(self.settings)

    def __setitem__(self, key, value):
        setitem(self._settings, key, value)
