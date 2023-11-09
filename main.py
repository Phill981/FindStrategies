import streamlit as st
import StockHandler as Sh
from strategies.TransitionStates import TransitionStates

def display_stock_info(stock_info):
    st.table(stock_info)

sh = Sh.StockHandler()
strategy = TransitionStates()

st.write("""
    # Get your Trades
         This is a small project, which help you analyze companies and backtracks their strategies
         """)

index = st.selectbox(
    'Which index would you like to analyze?',
    ('S&P 500', 'NASDAQ', 'DAX')
    )

option = st.selectbox(
    'Which strategy would you like to use to analyze your trades?',
    ('No Strategy', 'Transition Matrix')
)

trades = list()

if option == "No strategy":
    trades.clear()
elif(option == "Transition Matrix"):
    for ticker in sh.getTickers():
        strategyResult = strategy.startStrategy(ticker)
        if(strategyResult["status"]):
            del strategyResult["status"]
            trades += [strategyResult]
    display_stock_info(trades)
        

        


