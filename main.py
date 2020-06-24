#!/bin/env python3

import importlib
import time


def main():
    start = time.time()
    LOG_FILE = 'kmodes_log.txt'
    importlib.import_module('src.gui')

    elapsed_time = time.time() - start
    with open(LOG_FILE, 'w') as log:
        log.write('Total:\n' + str(elapsed_time) + 'seconds\n')

    importlib.import_module('src.tree_gui')


if __name__ == '__main__':
    main()
