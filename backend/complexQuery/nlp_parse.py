import spacy
from spacy.matcher import Matcher
from complexQuery.matcher_setup import patterns
from complexQuery.helper_funcs import *
nlp = spacy.load('en_core_web_sm')

def parse_query(query, locations, postcodes):
    doc = nlp(query)
    matcher = Matcher(nlp.vocab)
    
    # add punctuation to query for better catching
    if doc[-1].pos_ != 'PUNCT':
        if doc[0].pos_ == 'DET':
            newQuery = query + '?'
            doc = nlp(newQuery)
        elif doc[0].pos_ == 'NOUN' and doc[0].dep_ == 'compound':
            newQuery = query + '.'
            doc = nlp(newQuery)
    
    # add patterns to matcher and start matching
    for pattern_name in patterns.keys():
        matcher.add(pattern_name, patterns[pattern_name]['pattern'], on_match=patterns[pattern_name]['onMatch'])
    matches = matcher(doc)
    
    # go into specific functions and return
    if doc._.operationalq:
        if doc._.earlylate:
            return findEarliestOrLatestStore(locations=locations, open=doc._.open, early=doc._.early)
        elif doc._.atspecifictime:
            return findStoreSpecificTime(locations=locations, timestr=doc._.specifictime, open=doc._.open)
        elif doc._.openfor:
            return findStoreOperationalHours(locations=locations, hours=doc._.hours)
        elif doc._.openon:
            return findOpenStoresOnDay(locations=locations, day=doc._.day, open=doc._.open)
        elif doc._.longshort:
            return findStoreOperationalHours(locations=locations, hours=doc._.hours, longshort=True, long=doc._.long)
        else:
            print('operational no pass')
            return []
    elif doc._.locationq:
        return findStoresByStateCityPostcode(locations=locations, query=query, postcodes=postcodes)
    else:
        print('no pass')
        return []