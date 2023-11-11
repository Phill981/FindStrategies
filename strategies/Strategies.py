from strategies.TransitionStates import TransitionStates
from strategies.NewsImpact import NewsImpact
from dataclasses import dataclass
from typing import Callable

@dataclass
class Strategy:
    name: str
    strategy: Callable
    
class Strategies:
    transitionStates = TransitionStates()
    newsImpact = NewsImpact()
    
    strategies = [
        Strategy(
            "Transition States",
            transitionStates.startStrategy
            ),
        Strategy(
            "News Impact",
            newsImpact.startStrategy
        )
    ]
    
    def getStrategies(self)->list[Strategy]:
        return self.strategies
    
    def getFunction(self, name)->Callable:
        for strategy in self.strategies:
            if(strategy.name == name):
                return strategy.strategy
        return lambda *args: None