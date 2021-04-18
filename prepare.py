import pandas as pd
import numpy as np

import os
import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

# functions

def prep_create_labels(df):
    # removed rows without a description
    df = df[df.job_description != ''].reset_index(drop=True)

    # create a list that makes labels corresponding to the order of the original data
    ds = ['DS' for n in range(0,224)]
    da = ['DA' for n in range(0,223)]
    de = ['DE' for n in range(0,227)]
    mle = ['MLE' for n in range(0,224)]
    labels = ds + da + de + mle

    # Add labels column from the labels list
    df['label'] = labels

    # checking to be sure any stray jobs that aren't a target be removed
    df['valid'] = df.job_title.str.lower().str.extract(
        '(.*?data.*?scientist.*?|.*?data.*?analyst.*?|data.*?engineer.*?|.*?machine.*?learning.*?engineer.*?)')

    # storing null values in a separate DF
    null_rows = df[df.valid.isnull()]
    
    # Rowws to drop
    ds_drop = null_rows[0:4]
    de_drop = null_rows[null_rows.label == "DE"]

    # Rows to Keep
    mask = []

    for row in null_rows.job_title:
        if re.search(r'analyst', row, flags=re.IGNORECASE) != None:
            mask.append(True)
        else:
            mask.append(False)
    da_keep = null_rows[mask]
    
    # new variable
    mask = []

    for row in null_rows.job_title:
        if re.search(r'machine learning|learning engineer', row, flags=re.IGNORECASE) != None:
            mask.append(True)
        else:
            mask.append(False)

    mle_keep = null_rows[mask]

    # removing the orginal null_rows and reintroducing selected rows
    rows_to_keep = null_rows.drop(ds_drop.index).drop(de_drop.index)
    # drop original 58 that needed to be validated
    df = df.drop(null_rows.index)
    # merge the rows that we decided to keep and drop the valid column
    df = pd.concat([df, rows_to_keep]).drop(columns='valid')

    return df
