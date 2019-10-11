#!/usr/bin/python3
import os

class ChDir(object):
    def __init__(self, new_dir):
        self._new_dir = new_dir
        self._old_dir = os.getcwd()

    def __enter__(self):
        os.chdir(self._new_dir)

    def __exit__(self, *args):
        os.chdir(self._old_dir)