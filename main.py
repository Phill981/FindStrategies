import streamlit as st
from Watchlist import Watchlist
from strategies.TransitionStates import TransitionStates
import os

def filterTrades(trades, percentage:float)->list[dict]:
    filteredTrades = []
    for trade in trades:
        if(trade["probability"] >= percentage):
            filteredTrades += [trade]
    return filteredTrades 

def display_stock_info(stock_info:list[dict])->None:
    st.table(stock_info)
    
def getStrategies() ->list[str]:
    strategies = os.listdir("./strategies")
    strategies.remove("__pycache__")
    return [strategy for strategy in strategies]

watchlist = Watchlist()
strategy = TransitionStates()
trades:list[dict] = list()

st.write("""
    # Analyze your trades
         """)

index = st.selectbox(
    'Which index would you like to analyze?',
    ('S&P 500', 'NASDAQ', 'DAX')
    )

option = st.selectbox(
    'Which strategy would you like to use to analyze your trades?',
    ["No Strategy"] + getStrategies()
)


percentage = st.number_input(
    "Minimum probability wanted",
    max_value=1.0, min_value=0.0,
    step=.05) if option == "TransitionStates.py" else  0.0

buttonPress = st.button("Start", type="primary")

if buttonPress:
    if option == "No strategy":
        trades.clear()
    elif(option == "TransitionStates.py"):
        for ticker in watchlist.getTickers():
            strategyResult = strategy.startStrategy(ticker)
            if(strategyResult["status"]):
                del strategyResult["status"]
                if strategyResult["probability"] >= percentage:
                    trades += [strategyResult]
                    trades = filterTrades(trades, percentage)

if(len(trades) > 0):
    display_stock_info(trades)
