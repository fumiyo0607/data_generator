import pandas as pd
import numpy as np
import pickle
import os

color_list = ['coral', 'peachpuff', 'orange', 'teal', 'skyblue', 'mediumpurple', 'mediumvioletred', 'crimson']

def ensure_dir(dir: str):
    if not os.path.exists(dir):
        os.makedirs(dir)

def load(path):
    with open(path, 'rb') as f:
        load_data = pickle.load(f)
    return load_data

def save(path, data):
    """save data as pickle

    Args:
        path ([str]): path
        data ([any]): saving data
    """
    with open(path, 'wb') as f:
        pickle.dump(data , f)
    print('saved at {} '.format(path))