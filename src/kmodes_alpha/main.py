import importlib


def main():
    importlib.import_module('gui')
    importlib.import_module('src.tree_viz.tree_gui')


if __name__ == '__main__':
    main()
