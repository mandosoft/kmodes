import operator
from operator import itemgetter
import tkinter as tk
import sys 
import itertools 
import time 
import random

from collections import defaultdict
from tkinter import filedialog

from halo import Halo 

import pandas as pd
import numpy as np
from sklearn.metrics.cluster import adjusted_mutual_info_score as amis
from sklearn.metrics.cluster import normalized_mutual_info_score as nmis
from warnings import simplefilter


simplefilter(action='ignore', category=FutureWarning)


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
