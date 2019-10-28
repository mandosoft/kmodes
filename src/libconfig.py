import operator
import tkinter as tk
import sys 

from collections import defaultdict
from tkinter import filedialog

import pandas as pd
import numpy as np
from sklearn.metrics.cluster import adjusted_mutual_info_score as amis
from sklearn.metrics.cluster import normalized_mutual_info_score as nmis

def main():
    try:
        Logging.log(sys.version)
        import tkinter 
    except ImportError as error:
        # Output expected ImportErrors.
        Logging.log_exception(error)
        # Include the name and path attributes in output.
        Logging.log(f'error.name: {error.name}')
        Logging.log(f'error.path: {error.path}')
    except Exception as exception:
        # Output unexpected Exceptions.
        Logging.log_exception(exception, False)


if __name__ == "__main__":
    main()
