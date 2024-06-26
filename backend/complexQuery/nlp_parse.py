import spacy
from spacy.matcher import Matcher
from complexQuery.matcher_setup import patterns
from complexQuery.helper_funcs import *
nlp = spacy.load('en_core_web_sm')

# for debugging
# operationalQueries = [
#     "Which of the Subway stores close the latest?",
#     "What stores opens the earliest?",
#     "which stores closes the latest?",
#     "List stores that close the latest.",
#     "List stores that open the earliest.",
#     "List stores that close the latest",
#     "List stores that open the earliest",
#     "Which store open the earliest?",
#     "Which store close the latest?",
#     "Which store closes at 10PM?",
#     "Which store opens at 8AM?",
#     "Which stores are open 24 hours?",
#     "Which stores are open for 10 hours?",
#     "List stores that are open 24 hours.",
#     "List stores that are open for 10 hours.",
#     "List all stores that are open on weekends.",
#     "List all stores that are closed on weekends.",
#     "List stores that are closed on weekends.",
#     "Which stores are open on weekends?",
#     "Which stores are closed on weekends?",
#     "List all stores that are open on Mondays.",
#     "List all stores that are closed on Mondays.",
#     "List stores that are closed on Mondays.",
#     "Which stores are open on Mondays?",
#     "Which stores are closed on Mondays?",
#     "Which XYZ store has the shortest operating hours?",
#     "Which XYZ store has the longest operating hours?",
# ]

def parse_query(query, locations):
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
    
    for token in doc:
        print(f'Token: {token.text}, POS: {token.pos_}, Dependency: {token.dep_}, Head: {token.head.text}, Lemma: {token.lemma_}')
    
    # add patterns to matcher and start matching
    for pattern_name in patterns.keys():
        matcher.add(pattern_name, patterns[pattern_name]['pattern'], on_match=patterns[pattern_name]['onMatch'])
    matches = matcher(doc)
    
    # go into specific functions and return
    if doc._.operational:
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
    else:
        print('no pass')
        return []

# if __name__ == '__main__':
#     # print(spacy.explain('det'))
#     for q in operationalQueries:
#         print(f'Query: {q}')
#         parsed_data = parse_query(q, None)
#         # print(parsed_data)