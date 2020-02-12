import importlib


def main():
    importlib.import_module('gui')
    importlib.import_module('kmodes_alpha_h')
    importlib.import_module('preprocessor')
    importlib.import_module('tree_assembler')


if __name__ == '__main__':
    main()
