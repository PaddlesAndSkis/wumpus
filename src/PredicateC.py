# PredicateC

from pomegranate.distributions import Categorical
from pomegranate.distributions import ConditionalCategorical
from pomegranate.bayesian_network import BayesianNetwork

class PredicateC():   
    def __init__(self, prob: float):
        self.p = prob
        
    def toList(self):
        return [1-self.p, self.p]
        
    def toCategorical(self):
        return Categorical([self.toList()])





