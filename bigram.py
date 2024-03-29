#from lib2to3.pgen2.tokenize import tokenize
import os
import sqlite3
import pandas as pd
from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize
import nltk
#from nltk.util import ngrams
from collections import Counter

#import re

stop = set(stopwords.words('english'))


CON = sqlite3.connect(os.path.expanduser(
    "C:\GitHub\TLars\crec.db"))

CUR = CON.cursor()


MAIN_KEYWORD = r'climate\schange|global\swarming' # Reduce full db to keywords


def df_main():
    """Pull full database into dataframe"""
    reduced_df = pd.read_sql("Select * from Reduced", CON, index_col='UTC')
    reduced_df['html_data'] = reduced_df['html_data'].str.replace('\n', ' ')
    reduced_df['html_data'] = reduced_df['html_data'].str.lower()
    reduced_df['html_data'] = reduced_df['html_data'].str.replace('climate change', 'climatechange')
    reduced_df['html_data'] = reduced_df['html_data'].str.replace('global warming', 'globalwarming')
    #reduced_df = reduced_df.set_index(pd.DatetimeIndex(reduced_df.index)).loc[:'2021-12-31'] # (End Date?) Control date range of df
    return reduced_df


def df_clean():
    """Reduce database further by ignoring stopwords and punctuation"""
    clean_df = df_main()

    return bigram(clean_df)
    """
    for word in tokens:
        if word in stop:
            tokens.remove(word)
    print("Post Stop length: " + len(tokens))
    """
    """
    raw_reduced = clean_df.html_data.tolist()
    tokens = nltk.word_tokenize(str(raw_reduced))
    tokenized_reduced = nltk.Text(tokens)
    print("Words: " + str(len(tokenized_reduced)))
    tokenized_reduced.concordance("climate", lines=25)

    bigram_list = []
    for bg in list(nltk.bigrams(tokenized_reduced)):
        if 'climate' in bg or 'warming' in bg:
            if bg[0] not in stopwords and bg[1] not in stopwords:
                bigram_list.append(bg)

    bigrams_tagged = []
    for i in bigram_list:
        bigrams_tagged.append(nltk.pos_tag(i, tagset='universal'))
    
    print("Bigram list: " + print(len(bigram_list)))
    counter = Counter(bigram_list)
    counter.most_common()

    tagged_list =[]
    for i in bigrams_tagged:
        if i[0][1] == 'VERB' or i[1][1] == 'VERB':
            tagged_list.append(i)

    print("tagged: " + tagged_list)
    POS_list = []
    for sublist in tagged_list:
        for sub_sublist in sublist:
            POS_list.append(sub_sublist)
    print("POS list: " + POS_list)
    print("Most common: " + Counter(POS_list).most_common())
    return clean_df
"""


def bigram(reduced):
    reduced["tokenized"] = reduced["html_data"]
    reduced["tokenized"] = reduced["tokenized"].str.replace('[^\w\s]','')
    #print(reduced["tokenized"])
    #reduced['tokenized'] = reduced['tokenized'].apply(lambda x: [item for item in x if item not in stop])
    #print(reduced["tokenized"])
    reduced['tokenized'] = reduced.apply(lambda column: nltk.word_tokenize(column['tokenized']), axis=1)
    
    #print(reduced['tokenized']) 
    #print("Pre stop token length: ")
    #count(reduced['tokenized'])
    stop_array = []
    for day in reduced['tokenized']:
        day_array = []
        for word in day:
            if word in stop:
                day.remove(word)
        stop_array.append(day)

    reduced['stop'] = stop_array


    reduced['stop'] = reduced.apply(lambda column: list(nltk.ngrams(column['stop'], 2)), axis=1)
    
    #print(reduced['tokenized'])
    #print(reduced)
    bigram_list = []
    reducedWord = 0
    for day in reduced['stop']:
        reducedWord += len(day)
        for bg in day:   
            if 'climatechange' in bg or 'globalwarming' in bg:
                if bg[0] not in stop and bg[1] not in stop:
                    bigram_list.append(bg)
    
    #print("Bigram list: " + str(len(bigram_list)))
    #print(bigram_list)
    #print("ReducedWord:" + str(reducedWord))
    #print(bigram_list)
    counter = Counter(bigram_list)
    counter.most_common()
    #print(counter)
    df = pd.DataFrame({'bigram':counter}).reset_index()
    df = df.sort_values('bigram', ascending=False)
    print(df)
    #reduced['bigrams'] = bigram_list

    return df

def count(tokens):
    words = 0
    for day in tokens:
        words += len(day)
    print("Words: " + str(words))

#df_clean()
bigram(df_main()).to_sql('bigrams', CON, if_exists='replace')