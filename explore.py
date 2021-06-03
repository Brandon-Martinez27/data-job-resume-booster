import pandas as pd

import matplotlib.pyplot as plt

def words_by_label(df):
    # change words in each label into a list
    da_words = ' '.join(df[df.label == 'DA'].clean)
    ds_words = ' '.join(df[df.label == 'DS'].clean)
    de_words = ' '.join(df[df.label == 'DE'].clean)
    mle_words = ' '.join(df[df.label == 'MLE'].clean)
    all_words = ' '.join(df.clean) 

    # eliminate white space before and after text, then split 
    # into individual word strings
    da_words = re.sub(r'\s.\s', '', da_words).split()
    ds_words = re.sub(r'\s.\s', '', ds_words).split()
    de_words = re.sub(r'\s.\s', '', de_words).split()
    mle_words = re.sub(r'\s.\s', '', mle_words).split()
    all_words = re.sub(r'\s.\s', '', all_words).split()

    return da_words, ds_words, de_words, mle_words, all_words