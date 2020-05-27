#!/bin/env python3

import importlib


def main():
    importlib.import_module('src.gui')
    importlib.import_module('src.tree_gui')


if __name__ == '__main__':
    main()
