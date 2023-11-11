import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class NewsImpact:
    def __init__(self):
        self.tickers = []
        self.news_tables = {}
        self.analyzer = SentimentIntensityAnalyzer()

    def download_data(self, ticker):
        finwiz_url = 'https://finviz.com/quote.ashx?t='
        url = finwiz_url + ticker
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url=url, headers=headers)
        try:
            resp = urlopen(req)
        except:
            self.news_tables[ticker] = ""
        html = BeautifulSoup(resp, features="lxml")
        news_table = html.find(id='news-table')
        self.news_tables[ticker] = news_table

    def analyze_sentiment(self, ticker):
        parsed_news = []
        for file_name, news_table in self.news_tables.items():
            for x in news_table.findAll('tr'):
                text = x.a.get_text()
                date_scrape = x.td.text.split()

                if len(date_scrape) == 1:
                    time = date_scrape[0]
                else:
                    date = date_scrape[0]
                    time = date_scrape[1]

                parsed_news.append([ticker, date, time, text])

        columns = ['Ticker', 'Date', 'Time', 'Headline']
        news_df = pd.DataFrame(parsed_news, columns=columns)
        scores = news_df['Headline'].apply(self.analyzer.polarity_scores).tolist()

        df_scores = pd.DataFrame(scores)
        news_df = news_df.join(df_scores, rsuffix='_right')

        news_df['Date'] = pd.to_datetime(news_df['Date'], errors='coerce').dt.date
        return news_df

    def startStrategy(self, ticker):
        self.download_data(ticker)
        
        sentiment_df = self.analyze_sentiment(ticker)

        unique_ticker = sentiment_df['Ticker'].unique().tolist()
        news_dict = {name: sentiment_df.loc[sentiment_df['Ticker'] == name] for name in unique_ticker}

        values = []
        dataframe = news_dict[ticker]
        dataframe = dataframe.set_index('Ticker')

        if 'Headline' in dataframe.columns:
            dataframe = dataframe.drop(columns=['Headline'])

        mean = round(dataframe['compound'].mean(), 2)
        values.append(mean)

        df = pd.DataFrame(list(zip([ticker], values)), columns=['Ticker', 'Mean Sentiment'])
        temp = df.to_dict()
        trade = {
            "ticker" : temp["Ticker"][0],
            "sentiment" : temp["Mean Sentiment"][0]
        }
        return trade
