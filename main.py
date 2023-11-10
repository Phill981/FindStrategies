import streamlit as st
from Watchlist import Watchlist
from strategies.Strategies import Strategies

def getTopMoves(arr):
        orderedArray = []
        tradeArray = arr
        while len(tradeArray) > 0:
            maxIndex = 0
            for index in range(len(tradeArray)):
                if (tradeArray[index]["probability"] > tradeArray[maxIndex]["probability"]):
                    maxIndex = index
            orderedArray.append(tradeArray[maxIndex])
            del tradeArray[maxIndex]
        return orderedArray

def filterTrades(trades, percentage:float)->list[dict]:
    filteredTrades = []
    for trade in trades:
        if(trade["probability"] >= percentage):
            filteredTrades += [trade]
    return filteredTrades 

def display_stock_info(stock_info:list[dict])->None:
    st.table(stock_info)

watchlist = Watchlist()
strategies = Strategies()

trades:list[dict] = list()

st.write("""
    # Analyze your trades
         """)

# Select the index that shall be analyzed
index = st.selectbox(
    'Which index would you like to analyze?',
    ('S&P 500', 'NASDAQ', 'DAX')
    )

# Select the strategy to analyze the list
option = st.selectbox(
    'Which strategy would you like to use to analyze your trades?',
    ["No Strategy"] + [strategy.name for strategy in strategies.getStrategies()]
)

# If the transition matrix strategy is chosen, we need to dynamically 
# set the percentage. Hence, the number input 
percentage = st.number_input(
    "Minimum probability wanted",
    max_value=1.0, min_value=0.0,
    step=.05) if option == "Transition States" else  0.0

buttonPress = st.button("Start", type="primary")

if buttonPress:
    match option:
        case  "No strategy":
            trades.clear()
        case  "Transition States":
            strategy = strategies.getFunction("Transition States")
            # put this into a function when more methods have been added
            for ticker in watchlist.getTickers():
                
                strategyResult = strategy(ticker)
                if(strategyResult["status"]):
                    #the status is not needed anymore
                    del strategyResult["status"]
                    if strategyResult["probability"] >= percentage:
                        trades += [strategyResult]
                        trades = filterTrades(trades, percentage)
                        trades = getTopMoves(trades)[:13]

# Displaying the final table
if(len(trades) > 0):
    display_stock_info(trades)
