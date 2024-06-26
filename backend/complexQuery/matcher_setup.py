from spacy.tokens import Doc

Doc.set_extension('operational', default=False)
Doc.set_extension('earlylate', default=False)
Doc.set_extension('open', default=False)
Doc.set_extension('early', default=False)
Doc.set_extension('atspecifictime', default=False)
Doc.set_extension('specifictime', default='')
Doc.set_extension('openfor', default=False)
Doc.set_extension('hours', default=0)
Doc.set_extension('openon', default=False)
Doc.set_extension('day', default='')
Doc.set_extension('longshort', default=False)
Doc.set_extension('long', default=False)

def set_operational_true(matcher, doc, i, matches):
    doc._.operational = True
    
def set_earlylate_true(matcher, doc, i, matches):
    doc._.earlylate = True
    match_id, start, end = matches[i]
    if doc[start].lemma_.lower() == 'open':
        doc._.open = True
    if doc[end-1].text.lower() == 'earliest':
        doc._.early = True
    
def set_atspecifictime_true(matcher, doc, i, matches):
    doc._.atspecifictime = True
    match_id, start, end = matches[i]
    if start == end - 4:
        doc._.specifictime = doc[start+2].text +':00'+ doc[start+3].text
    elif start == end - 3:
        doc._.specifictime = doc[start+2].text
        
    if doc[start].text.lower() == 'opens' or doc[start].text.lower() == 'open':
        doc._.open = True
    
def set_openfor_true(matcher, doc, i, matches):
    doc._.openfor = True
    match_id, start, end = matches[i]
    doc._.hours = int(doc[end-2].text)
    
def set_openon_true(matcher, doc, i, matches):
    doc._.openon = True
    match_id, start, end = matches[i]
    doc._.day = doc[end-1].text
    
    if doc[start].text.lower() == 'open':
        doc._.open = True
    
def set_longshort_true(matcher, doc, i, matches):
    doc._.longshort = True
    match_id, start, end = matches[i]
    if doc[start].text.lower() == 'longest':
        doc._.long = True
    
# add patterns to match here
patterns = {
    'pattern_operational_closesopens': {
        'pattern': [
            [
                {
                    "LEMMA": {"IN": ["close", "open", "store"]},
                    "DEP": "ROOT"
                }
            ]
        ],
        'onMatch': set_operational_true
    },
    'pattern_operational_areopen': {
        'pattern': [
            [
                {
                    "LEMMA": "be",
                    "DEP": "ROOT"
                },
                {
                    "LEMMA": "open",
                    "DEP": "acomp"
                }
            ]
        ],
        'onMatch': set_operational_true
    },
    'pattern_operational_list': {
        'pattern': [
            [
                {
                    "LOWER": "list",
                    "DEP": "ROOT"
                },
                {
                    "LOWER": "all",
                    "DEP": "det"
                },
                {
                    "LEMMA": "store",
                    "DEP": "dobj"
                }
            ]
        ],
        'onMatch': set_operational_true
    },
    'pattern_operational_operatinghour': {
        'pattern': [
            [
                {
                    "LOWER": "operating",
                    "DEP": "compound"
                },
                {
                    "LEMMA": "hour",
                    "DEP": "dobj"
                }
            ]
        ],
        'onMatch': set_operational_true
    },
    'pattern_earlylate': {
        'pattern': [
            [
                {
                    "LEMMA": {"IN": ["close", "open"]},
                    "POS": "VERB"
                },
                {
                    "LOWER": "the",
                    "DEP": "det"
                },
                {
                    "LOWER": {"IN": ["earliest", "latest"]}, 
                    "DEP": "dobj"
                }
            ]
        ],
        'onMatch': set_earlylate_true
    },
    'pattern_atspecifictime': {
        'pattern': [
            [
                {
                    "LOWER": {"IN": ["opens","closes","open","close"]},
                    "POS": "VERB"
                },
                {
                    "LOWER": "at",
                    "DEP": "prep"
                },
                {
                    "POS": "NUM"
                },
                {
                    "POS": "NOUN",
                    "DEP": {"IN": ["pobj","dobj"]}
                }
            ],
            [
                {
                    "LOWER": {"IN": ["opens","closes","open","close"]},
                    "POS": "VERB"
                },
                {
                    "LOWER": "at",
                    "DEP": "prep"
                },
                {
                    "POS": "NUM",
                    "DEP": "pobj"
                }
            ]
        ],
        'onMatch': set_atspecifictime_true
    },
    'pattern_openfor': {
        'pattern': [
            [
                {
                    "LEMMA": "be",
                    "DEP": "ROOT"
                },
                {
                    "LEMMA": "open",
                },
                {
                    "LOWER": "for",
                },
                {
                    "POS": "NUM",
                    "DEP": "nummod"
                },
                {
                    "LOWER": {"IN": ["hour", "hours"]},
                    "POS": "NOUN",
                    "DEP": "pobj"
                }
            ],
            [
                {
                    "LEMMA": "be",
                    "DEP": "ROOT"
                },
                {
                    "LEMMA": "open",
                },
                {
                    "POS": "NUM",
                    "DEP": "nummod"
                },
                {
                    "LOWER": {"IN": ["hour", "hours"]},
                    "POS": "NOUN",
                    "DEP": "npadvmod"
                }
            ],
            [
                {
                    "LEMMA": "be",
                    "DEP": "relcl"
                },
                {
                    "LEMMA": "open",
                },
                {
                    "POS": "NUM",
                    "DEP": "nummod"
                },
                {
                    "LOWER": {"IN": ["hour", "hours"]},
                    "POS": "NOUN",
                    "DEP": "npadvmod"
                }
            ],
            [
                {
                    "LEMMA": "be",
                    "DEP": "relcl"
                },
                {
                    "LEMMA": "open",
                },
                {
                    "LOWER": "for",
                },
                {
                    "POS": "NUM",
                    "DEP": "nummod"
                },
                {
                    "LOWER": {"IN": ["hour", "hours"]},
                    "POS": "NOUN",
                    "DEP": "pobj"
                }
            ],
        ],
        'onMatch': set_openfor_true
    },
    'pattern_openon': {
        'pattern': [
            [
                {
                    "LOWER": {"IN": ["open","closed"]}
                },
                {
                    "LOWER": "on",
                    "DEP": "prep",
                },
                {
                    "POS": "NOUN",
                    "DEP": "pobj"
                }
            ],
            [
                {
                    "LOWER": {"IN": ["open","closed"]}
                },
                {
                    "LOWER": "on",
                    "DEP": "prep",
                },
                {
                    "POS": "PROPN",
                    "DEP": "pobj"
                }
            ]
        ],
        'onMatch': set_openon_true
    },
    'pattern_longshort': {
        'pattern': [
            [
                {
                    "LOWER": {"IN": ["longest", "shortest"]},
                    "DEP": "amod",
                    "POS": "ADJ"
                },
                {
                    "LOWER": "operating",
                    "DEP": "compound"
                },
                {
                    "LEMMA": "hour",
                    "DEP": "dobj"
                }
            ]
        ],
        'onMatch': set_longshort_true
    },
}