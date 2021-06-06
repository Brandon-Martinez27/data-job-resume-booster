import pandas as pd
import re
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

def freq_by_label(da_words, ds_words, de_words, mle_words, all_words):
    # transform each label string into a pandas Series
    da_freq = pd.Series(da_words).value_counts()
    ds_freq = pd.Series(ds_words).value_counts()
    de_freq = pd.Series(de_words).value_counts()
    mle_freq = pd.Series(mle_words).value_counts()
    all_freq = pd.Series(all_words).value_counts()

    return da_freq, ds_freq, de_freq, mle_freq, all_freq

def word_count_label(da_freq, ds_freq, de_freq, mle_freq, all_freq):
    # combine all into a dataframe to work with
    word_counts = (pd.concat([all_freq, ds_freq, da_freq, de_freq, mle_freq], axis=1, sort=True)
                    .set_axis(['all', 'DS', 'DA', 'DE', 'MLE'], axis=1, inplace=False)
                    .fillna(0)
                    .apply(lambda s: s.astype(int)))
    # add the proportion of each label in relation to all other categories
    word_counts['prop_ds'] = word_counts['DS']/word_counts['all']
    word_counts['prop_da'] = word_counts['DA']/word_counts['all']
    word_counts['prop_de'] = word_counts['DE']/word_counts['all']
    word_counts['prop_mle'] = word_counts['MLE']/word_counts['all']

    return word_counts