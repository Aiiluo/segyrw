""" 
This is a shell for test the panda model of python 

Author:chenp
"""
print(__doc__)

from pandas import DataFrame, Series
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

excel_path = 'excel.xlsx'
data = pd.read_excel(excel_path, sheetname=None)
print(data)
