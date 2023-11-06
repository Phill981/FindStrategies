import streamlit as st
import StockHandler as Sh
import requests
from bs4 import BeautifulSoup




sh = Sh.StockHandler()

st.write("""
    # Markov Chain Analyze your Company
    
         This is a small project, which help you analyze companies and backtracks their strategies
         """)

ticker = st.text_input('What stock do you want to analyze?', 'AAPL')
wantedPercent = st.text_input('How much percent should a transition have to be highlighted?', '60')

df = sh.dataframeMatrix(ticker)
df5 = sh.createFiveDayMatrix(ticker)

st.write(f"""    
    ## Analytics and Transition Matrix of {ticker} 
         """)

st.write("""    
    ### Transition matrix - 1 day
         """)
st.dataframe(
        df,
        use_container_width=True
        )

st.write("""
    ### Transition matrix - 5 days
         """)
st.dataframe(
        df5,
        use_container_width=True
        )
