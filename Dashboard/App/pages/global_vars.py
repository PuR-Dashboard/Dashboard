import pandas as pd
from utility.util_functions import get_data
from collections import defaultdict

global data, current_filter
data = None
current_filter = None

def init():
    #print("initialize")
    global data
    data = get_data(name_of_csv="Characteristics.csv")
    
    global current_filter
    current_filter = defaultdict(lambda: None)