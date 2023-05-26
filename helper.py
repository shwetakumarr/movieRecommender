import numpy as np
import pandas as pd

def read_files(fname):
    temp = pd.read_csv(fname, sep=';')

    return temp

