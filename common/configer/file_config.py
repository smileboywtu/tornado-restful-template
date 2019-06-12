# -*- coding: utf-8 -*-

"""


use python file to config


"""
import hashlib
import importlib
import json
import os
from operator import setitem, itemgetter, attrgetter

import yaml


class Config:
    _settings = {}

    def __init__(self, file_path):
        self._load_file(file_path)
        self._load_environ()

    def _load_file(self, file_path):
        raise NotImplemented

    def _load_environ(self):
        """
        environment start with APP_
        :return:
        """
        raise NotImplemented

    def reload(self, file_path):
        self._load_file(file_path)
        self._load_environ()

    def update_from_file(self, file_path):
        self._load_file(file_path)

    def update_from_environ(self):
        self._load_environ()

    @property
    def settings(self):
        return self._settings

    def __getitem__(self, item):
        return self._settings[item]

    def __setitem__(self, key, value):
        self._settings[key] = value

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value


class FileConfigPy(Config):

    def __init__(self, file_path):
        super(FileConfigPy, self).__init__(file_path)

    def _load_file(self, file_path):
        variables = importlib.import_module(file_path.rstrip(".py"))
        for item in dir(variables):
            if not item.startswith("__"):
                self[item] = attrgetter(item)(variables)

    def _load_environ(self):
        """
        environment start with APP_
        :return:
        """
        # for key, value in os.environ.items():
        #     if key.startswith("APP_"):
        #         self._settings[key] = value
        for k, v in os.environ.items():
            if k in self._settings:
                try:
                    self[k] = eval(v)
                except (NameError, SyntaxError):
                    self[k] = v
            else:
                self[k] = v


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
        # for key, value in os.environ.items():
        #     if key.startswith("APP_"):
        #         self._settings[key] = value
        self._settings.update(os.environ)

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


config = FileConfigPy("config.py")
