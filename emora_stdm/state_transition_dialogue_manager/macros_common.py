
from emora_stdm.state_transition_dialogue_manager.macro import Macro
from emora_stdm.state_transition_dialogue_manager.ngrams import Ngrams
from typing import Union, Set, List, Dict, Callable, Tuple, NoReturn, Any
import nltk
try:
    nltk.data.find('wordnet')
except:
    nltk.download('wordnet')

class ONTE(Macro):
    """
    get the set of expressions matching the entire descendent subree
    underneath a given set of ontology nodes (usually 1)
    """
    def __init__(self, kb):
        self.kb = kb
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
        self.lemmatizer.lemmatize('initialize')
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        node_set = args[0]
        ont_result = self.kb.expressions(self.kb.subtypes(node_set))
        if ngrams:
            lemmas = {self.lemmatizer.lemmatize(gram): gram for gram in ngrams}
            matches = lemmas.keys() & ont_result
            return {lemmas[match] for match in matches}
        else:
            return ont_result

class KBE(Macro):
    """
    get the set of expressions matching the nodes returned from a KB
    query, where the first arg is a set of starting nodes (or single node)
    and each following arg is a (set or single) relation to traverse
    """
    def __init__(self, kb):
        self.kb = kb
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
        self.lemmatizer.lemmatize('initialize')
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        kb_result = self.kb.expressions(self.kb.query(*args))
        if ngrams:
            lemmas = {self.lemmatizer.lemmatize(gram): gram for gram in ngrams}
            matches = lemmas.keys() & kb_result
            return {lemmas[match] for match in matches}
        else:
            return kb_result

class EXP(Macro):
    def __init__(self, kb):
        self.kb = kb
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
        self.lemmatizer.lemmatize('initialize')
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        kb_result = self.kb.expressions(*args)
        if ngrams:
            lemmas = {self.lemmatizer.lemmatize(gram): gram for gram in ngrams}
            matches = lemmas.keys() & kb_result
            return {lemmas[match] for match in matches}
        else:
            return kb_result
