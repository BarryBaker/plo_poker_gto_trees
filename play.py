import numpy as np
import pandas as pd
import pickle
import glob
import os
from icecream import ic as qw
import json
from scipy.stats import pointbiserialr

a = [("a", "b"), ("a", "c")]
print(a == [("a", "b"), ("a", "c")])

a = [i for i in [1, 2, 3] if i == 4]
print(a == [])
