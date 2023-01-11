import pandas as pd
import numpy as np
import unicodedata
import re
from bs4 import BeautifulSoup
import acquire as a
import requests

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords


def basic_clean(input_string):
    '''
    basice_clean function takes in a string and performs the following cleaning: lowercase, normalize characters
    and replaces anything that ia a letter , number, whitespace or sigle quote
    returns clean_string
    '''
    # takes original string and lowercase the string
    clean_string = input_string.lower()
    
    # normalized the string
    clean_string = unicodedata.normalize('NFKD', clean_string).encode('ascii','ignore').decode('utf-8')
    
    # remove anything that is not a through z, a number, a single quote, or whites
    clean_string = re.sub(r"[^a-z0-9'\s]", '', clean_string)
    
    return clean_string

def tokenize(input_string,return_str = True):
    '''
    tokenize takes in a string and passes throug basic_clean function then tokenize all the words in the string
    returns token_string
    '''

    # create tokenizer object
    tokenizer = nltk.tokenize.ToktokTokenizer()
     
    # apply token to string    
    token_string  = tokenizer.tokenize(input_string, return_str=return_str)

    
    return token_string

def stem(input_string):
    '''
    stem takes in a string 
    returns stem_string a stem version of string
    '''
    # create stemming object
    ps = nltk.porter.PorterStemmer()
    # stemming string
    stem_string = [ps.stem(word) for word in input_string.split()]
    # join stemmed string
    stem_string = ' '.join(stem_string)
    
    return stem_string

def lemmatize(input_string):
    '''
    lemmatize takes in a string 
    returns lemmas_string a lemmatize version of the string.
    '''
    
    # create object
    wnl = nltk.stem.WordNetLemmatizer()
    
    # apply lemmatizer to string
    lemmas_string = [wnl.lemmatize(word) for word in input_string.split()]
    lemmas_string = " ".join(lemmas_string)
    
    return lemmas_string

def remove_stopwords(input_string, extra_words = [],exclude_words = []):
    '''
    remove_stopwords takes in a string, optional extra_words as a list and exclude_words as a list
    parameters with default  empty lists and returna string.
    '''
    
    # ceate stopwords list
    stopwords_list = stopwords.words('english')
    
    # take out some words
    stopwords_list = set(stopwords_list)-set(exclude_words)
    
    # words to be added
    stopwords_list = stopwords_list.union(set(exclude_words))
    
    # split our document by spaces
    words = input_string.split()
    
    # this is the stopwords applied(taken out of) the original text
    new_string = [word for word in input_string.split() if word not in stopwords_list]
    # join together
    new_string = ' '.join(new_string)

    return new_string

def get_blog_urls(base_url, header={'User-Agent': 'hamsandwich'}):
    soup = BeautifulSoup(requests.get(base_url, headers=header).content)
    return [link['href'] for link in soup.select('a.more-link')]

def get_blog_content(base_url,header):
    blog_links = get_blog_urls(base_url)
    all_blogs = []
    for blog in blog_links:
        blog_soup = BeautifulSoup(
            requests.get(blog,
                headers=header).content)
        blog_content = {'title': blog_soup.select_one(
            'h1.entry-title').text,
        'content': blog_soup.select_one(
            'div.entry-content').text.strip()}
        all_blogs.append(blog_content)
    return all_blogs