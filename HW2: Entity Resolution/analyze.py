import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
 
def get_google_catalog():
    return pd.read_csv('GoogleProducts.csv')
 
def get_amazon_catalog():
    return pd.read_csv('Amazon.csv')

#A Function to break a string into qgrams (q-character tokens)
#we'll pad the string with spaces on the front and end
def qgram(str,q):
    str = ' ' + str + ' '
    return([str[i:i+q] for i in range(len(str)-(q-1))])
 
#compute the jaccard similarity of two strings using qgrams
#pass in a value for q to do anything other than bi-grams
#call jaccard_simq with verbose set to True to see intermediate values
 
def jaccard_simq(str1, str2,q=2):
    set1 = set(qgram(str1,q))
    set2 = set(qgram(str2,q))
    common_tokens = set1.intersection(set2)
    all_tokens = set1.union(set2)
    return float(len(common_tokens) / len(all_tokens))
 
def match():
   '''
   Match must return a list of tuples of amazon ids and google ids.
   For example:
   [('b000jz4hqo', http://www.google.com/base/feeds/snippets/11125907881740407428'),....]
   '''
   google_df = get_google_catalog()
   amazon = get_amazon_catalog()
   formatted_df = google_df.loc[google_df['price'].str.contains('gbp')]['price'].str.split('gbp', expand=True)
   formatted_df.drop(formatted_df.columns[1], axis=1, inplace=True)
   formatted_df.astype(float)

   for i in range(len(formatted_df.index)):
       google_df['price'][formatted_df.index[i]] = formatted_df.iloc[i]
   
   google_df['price'].astype(float)
   google_sorted = google_df.sort_values(by='name')
   amazon_sorted = amazon.sort_values(by='title')
   
   amazon_unique = amazon_sorted.drop_duplicates()
   count = 0
   final_list = []
   for i in range(len(amazon_unique)):
        tup_list = []
        count += 1
        price_df = google_df.loc[abs(google_df['price'].astype(float) - amazon_unique['price'].iloc[i].astype(float)) / amazon_unique['price'].iloc[i].astype(float) < 0.5]

        for j in range(len(price_df)):
            sim = fuzz.partial_ratio(price_df['name'].iloc[j], amazon_unique['title'].iloc[i])
            if (sim >= 40):
                if (sim >= 60):
                    if (len(tup_list) != 0):
                        for w in range(len(tup_list)):
                            if (amazon_unique['id'].iloc[i] == tup_list[w][0]):
                                if sim > tup_list[w][2]:
                                    tup_list.pop(w)
                                    tup_list.append((amazon_unique['id'].iloc[i], price_df['id'].iloc[j], sim))
                                else:
                                    continue
                            else:
                                tup_list.append((amazon_unique['id'].iloc[i], price_df['id'].iloc[j], sim))
                    else:
                        tup_list.append((amazon_unique['id'].iloc[i], price_df['id'].iloc[j], sim))
                elif not(pd.isna(amazon_unique['manufacturer'].iloc[i])) and not(pd.isna(price_df['manufacturer'].iloc[j])):
                    price_sim = abs(amazon_unique['price'].astype(float).iloc[i] - price_df['price'].astype(float).iloc[j]) / amazon_unique['price'].astype(float).iloc[i]
                    if price_sim < 0.3:
                        if (len(tup_list) != 0):
                            for w in range(len(tup_list)):
                                if (amazon_unique['id'].iloc[i] == tup_list[w][0]):
                                    if sim > tup_list[w][2]:
                                        tup_list.pop(w)
                                        tup_list.append((amazon_unique['id'].iloc[i], price_df['id'].iloc[j], sim))
                                    else:
                                        continue
                                else:
                                    tup_list.append((amazon_unique['id'].iloc[i], price_df['id'].iloc[j], sim))
                        else:
                            tup_list.append((amazon_unique['id'].iloc[i], price_df['id'].iloc[j], sim))               
                    else:
                        man_sim = jaccard_simq(amazon_unique['manufacturer'].iloc[i], price_df['manufacturer'].iloc[j])
                        if man_sim >= 0.7:
                            if (len(tup_list) != 0):
                                for w in range(len(tup_list)):
                                    if (amazon_unique['id'].iloc[i] == tup_list[w][0]):
                                        if sim > tup_list[w][2]:
                                            tup_list.pop(w)
                                            tup_list.append((amazon_unique['id'].iloc[i], price_df['id'].iloc[j], sim))
                                        else:
                                            continue
                                    else:
                                        tup_list.append((amazon_unique['id'].iloc[i], price_df['id'].iloc[j], sim))
                            else:
                                tup_list.append((amazon_unique['id'].iloc[i], price_df['id'].iloc[j], sim))

        for tup in tup_list:
            pair = (tup[0], tup[1])
            final_list.append(pair)

   return final_list
    
    
match()