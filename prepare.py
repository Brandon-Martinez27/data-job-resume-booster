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


def basic_clean(string):
    '''
    This function takes in a string and
    returns the string normalized.
    '''
    string = unicodedata.normalize('NFKD', string)\
             .encode('ascii', 'ignore')\
             .decode('utf-8', 'ignore')
    string = re.sub(r'[^\w\s]', '', string).lower()
    return string

##############################

def tokenize(string):
    '''
    This function takes in a string and
    returns a tokenized string.
    '''
    # Create tokenizer.
    tokenizer = nltk.tokenize.ToktokTokenizer()
    
    # Use tokenizer
    string = tokenizer.tokenize(string, return_str=True)
    
    return string

#############################

def stem(string):
    '''
    This function takes in a string and
    returns a string with words stemmed.
    '''
    # Create porter stemmer.
    ps = nltk.porter.PorterStemmer()
    
    # Use the stemmer to stem each word in the list of words we created by using split.
    stems = [ps.stem(word) for word in string.split()]
    
    # Join our lists of words into a string again and assign to a variable.
    string = ' '.join(stems)
    
    return string

#############################


def lemmatize(string):
    '''
    This function takes in string for and
    returns a string with words lemmatized.
    '''
    # Create the lemmatizer.
    wnl = nltk.stem.WordNetLemmatizer()
    
    # Use the lemmatizer on each word in the list of words we created by using split.
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    
    # Join our list of words into a string again and assign to a variable.
    string = ' '.join(lemmas)
    
    return string

#############################


def remove_stopwords(string, extra_words=[], exclude_words=[]):
    '''
    This function takes in a string, optional extra_words and exclude_words parameters
    with default empty lists and returns a string.
    '''
    # Create stopword_list.
    stopword_list = stopwords.words('english')
    
    # Remove 'exclude_words' from stopword_list to keep these in my text.
    stopword_list = set(stopword_list) - set(exclude_words)

    # Add in 'extra_words' to stopword_list.
    stopword_list = stopword_list.union(set(extra_words))
    
    # Split words in string.
    words = string.split()
    
    # Create a list of words from my string with stopwords removed and assign to variable.
    filtered_words = [word for word in words if word not in stopword_list]
    
    # Join words in the list back into strings and assign to a variable.
    string_without_stopwords = ' '.join(filtered_words)
    
    return string_without_stopwords

###############################


def prep_job_data(df, column, extra_words=[], exclude_words=[]):
    '''
    This function take in a df and the string name for a text column with 
    option to pass lists for extra_words and exclude_words and
    returns a df with the text article title, original text, stemmed text,
    lemmatized text, cleaned, tokenized, & lemmatized text with stopwords removed.
    '''
    # drops duplicates but keeps the first instance
    df = df.drop_duplicates(subset=None, keep='first')

    df['clean'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)\
                            .apply(lemmatize)
    
    df['stemmed'] = df[column].apply(basic_clean).apply(stem)
    
    df['lemmatized'] = df[column].apply(basic_clean).apply(lemmatize)
    
    return df[['language', 'repo', column, 'stemmed', 'lemmatized', 'clean']]



def add_columns(df):
    # add a column that is a list of each word for each repo 
    words = [re.sub(r'([^a-z0-9\s]|\s.\s)', '', doc).split() for doc in df.clean] 

    # column name will be words, and the column will contain lists of the words in each doc
    df = pd.concat([df, pd.DataFrame({'words': words})], axis=1)

    # add a column that shows the length 
    df['doc_length'] = [len(wordlist) for wordlist in df.words]
    return df

def split_repo_data(df):
    from sklearn.model_selection import train_test_split

    train_validate, test = train_test_split(df[['language', 
                            'clean', 'words', 'doc_length']], 
                                        stratify=df.language, 
                                        test_size=.2, 
                                        random_state=123)

    train, validate = train_test_split(train_validate, 
                                   stratify=train_validate.language, 
                                   test_size=.25,
                                   random_state=123)
    return train, validate, test
