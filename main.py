import streamlit as st
import StockHandler as Sh
from strategies.TransitionStates import TransitionStates
import os

def filterTrades(trades, percentage):
    filteredTrades = []
    for trade in trades:
        if(trade["probability"] >= percentage):
            filteredTrades += [trade]
    return filteredTrades 

def display_stock_info(stock_info):
    st.table(stock_info)
    
def getStrategies():
    strategies = os.listdir("./strategies")
    strategies.remove("__pycache__")
    return [strategy for strategy in strategies]

sh = Sh.StockHandler()
strategy = TransitionStates()
trades = list()

st.write("""
    # Get your Trades
         This is a small project, which help you analyze companies and backtracks their strategies
         """)

index = st.selectbox(
    'Which index would you like to analyze?',
    ('S&P 500', 'NASDAQ', 'DAX')
    )

buttonPress = st.button("Start", type="primary")

option = st.selectbox(
    'Which strategy would you like to use to analyze your trades?',
    ["No Strategy"] + getStrategies()
)

percentage = st.number_input(
    "Minimum probability wanted",
    max_value=1.0, min_value=0.0,
    step=.05
)
print(buttonPress)
if buttonPress:
    if option == "No strategy":
        trades.clear()
    elif(option == "TransitionStates.py"):
        for ticker in sh.getTickers():
            strategyResult = strategy.startStrategy(ticker)
            if(strategyResult["status"]):
                del strategyResult["status"]
                if strategyResult["probability"] >= percentage:
                    trades += [strategyResult]

displayTrades = filterTrades(trades, percentage)
if(len(displayTrades) > 0):
    display_stock_info(displayTrades)
