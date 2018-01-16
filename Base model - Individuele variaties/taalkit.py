from collections import namedtuple
from random import random

# An exemplar has a verb feature ('Vf' or 'Aux') and an adverb feature ('THEN' or 'AdvO').
Exemplar = namedtuple('Exemplar', ['verb', 'adverb'])

# An utterance consists of an exemplar and a V2 assignment (i.e., V2 or not V2).
Utterance = namedtuple('Utterance', ['exemplar', 'V2'])

class FreqPair:
    '''Represents a total number of utterances, plus how many are V2.'''

    def __init__(self, V2=0, Total=0):
        self.V2 = V2
        self.Total = Total

    def __add__(self, other):
        '''Returns the sum of two frequency pairs.'''
        return FreqPair(self.V2 + other.V2, self.Total + other.Total)

    def __sub__(self, other):
        '''Returns the difference between two frequency pairs.'''
        return FreqPair(self.V2 - other.V2, self.Total - other.Total)

    def __repr__(self):
        '''Returns an informative string representation of a frequency pair (typically called by print).'''
        return 'FreqPair(V2={0.V2}, Total={0.Total})'.format(self)

    def V2_fraction(self):
        '''Returns the fraction of V2 utterances.'''
        if self.Total == 0:
            return 1 #TODO: fix Ugly trick to prevent devision by 0
        return self.V2 / self.Total
        
    def copy(self):
      return FreqPair(self.V2, self.Total)

class FrequencyTable:
    '''Represents utterance frequencies in various feature combinations.'''

    def __init__(self):
        '''Creates a new, empty frequency table.'''
        self.Vf_THEN = FreqPair()
        self.Vf_AdvO = FreqPair()
        self.Aux_THEN = FreqPair()
        self.Aux_AdvO = FreqPair()

    @property
    def Vf(self):
        return self.Vf_THEN + self.Vf_AdvO

    @property
    def Aux(self):
        return self.Aux_THEN + self.Aux_AdvO

    @property
    def THEN(self):
        return self.Vf_THEN + self.Aux_THEN

    @property
    def AdvO(self):
        return self.Vf_AdvO + self.Aux_AdvO

    @property
    def Total(self):
        return self.Vf_THEN + self.Vf_AdvO + self.Aux_THEN + self.Aux_AdvO

    def random_exemplar(self):
        '''Returns a random exemplar based on the current utterance frequencies.'''
        p = random()
        total = self.Total.Total
        if total == 0:
            total = .00001  #TODO: ugly fix. Find solution
        if p < self.Vf_THEN.Total / total:
            return Exemplar(verb='Vf', adverb='THEN')
        elif p < (self.Vf_THEN.Total + self.Vf_AdvO.Total) / total:
            return Exemplar(verb='Vf', adverb='AdvO')
        elif p < (self.Vf_THEN.Total + self.Aux_THEN.Total + self.Aux_THEN.Total) / total:
            return Exemplar(verb='Aux', adverb='THEN')
        else:
            return Exemplar(verb='Aux', adverb='AdvO')

    def random_utterance(self):
        '''Returns a random utterance based on the current frequencies.'''
        p = random()
        total = self.Total.Total
        if p < self.Vf_THEN.Total / total:
            p_v2 = self.Vf_THEN.V2_fraction()
            v2 = random() < p_v2
            return Utterance(Exemplar(verb='Vf', adverb='THEN'), v2)
        elif p < (self.Vf_THEN.Total + self.Vf_AdvO.Total) / total:
            p_v2 = self.Vf_AdvO.V2_fraction()
            v2 = random() < p_v2
            return Utterance(Exemplar(verb='Vf', adverb='AdvO'), v2)
        elif p < (self.Vf_THEN.Total + self.Aux_THEN.Total + self.Aux_THEN.Total) / total:
            p_v2 = self.Aux_THEN.V2_fraction()
            v2 = random() < p_v2
            return Utterance(Exemplar(verb='Aux', adverb='THEN'), v2)
        else:
            p_v2 = self.Aux_AdvO.V2_fraction()
            v2 = random() < p_v2
            return Utterance(Exemplar(verb='Aux', adverb='AdvO'), v2)

    def add_utterance(self, utterance):
        '''Update the frequencies by adding one utterance.'''
        exemplar, V2 = utterance
        if exemplar == ('Vf', 'THEN'):
            self.Vf_THEN += FreqPair(1 if V2 else 0, 1)
        elif exemplar == ('Vf', 'AdvO'):
            self.Vf_AdvO += FreqPair(1 if V2 else 0, 1)
        elif exemplar == ('Aux', 'THEN'):
            self.Aux_THEN += FreqPair(1 if V2 else 0, 1)
        else:
            self.Aux_AdvO += FreqPair(1 if V2 else 0, 1)

    def remove_utterance(self, utterance):
        '''Update the frequencies by removing one utterance.'''
        exemplar, V2 = utterance
        if exemplar == ('Vf', 'THEN'):
            self.Vf_THEN -= FreqPair(1 if V2 else 0, 1)
        elif exemplar == ('Vf', 'AdvO'):
            self.Vf_AdvO -= FreqPair(1 if V2 else 0, 1)
        elif exemplar == ('Aux', 'THEN'):
            self.Aux_THEN -= FreqPair(1 if V2 else 0, 1)
        else:
            self.Aux_AdvO -= FreqPair(1 if V2 else 0, 1)


def read_frequencies(filename):
    '''Read historical frequencies from a disk file.'''
    freq = FrequencyTable()
    with open(filename) as source:
        data = source.read().splitlines()
    for line in data[1:]:
        verb, adverb, v2, total = line.split()
        pair = verb + '_' + adverb
        v2 = int(v2)
        total = int(total)
        if pair == 'Vf_THEN':
            freq.Vf_THEN = FreqPair(v2, total)
        elif pair == 'Vf_AdvO':
            freq.Vf_AdvO = FreqPair(v2, total)
        elif pair == 'Aux_THEN':
            freq.Aux_THEN = FreqPair(v2, total)
        elif pair == 'Aux_AdvO':
            freq.Aux_AdvO = FreqPair(v2, total)
    return freq
