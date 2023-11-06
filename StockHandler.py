import yfinance as yf
import json
import pandas as pd
import numpy as np
from pprint import pprint
class StockHandler:
    def __init__(self) -> None:
        self.tickers = self._readWatchlist() 

    def _readWatchlist(self):
        with open("watchlist.json", "r") as jfile:
            data = json.load(jfile)
        return data["stock"]        
    
    def getTickers(self):
        return self.tickers
    
    def addTickerToWatchlist(self, newTicker):
        try:
            with open("watchlist.json", "r") as jfile:
                data = json.load(jfile)
                data["stock"].append(newTicker)
            with open("watchlist.json", "w") as jfile:
                jObj = json.dumps(data)
                jfile.write(jObj)
        except FileNotFoundError:
            print("File 'watchlist.json' not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON data.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def removeTickerFromWatchlist(self, ticker):
        with open("watchlist.json", "r") as jfile:
            data = json.load(jfile)
            try:
                index = data["stock"].index(ticker)
                del data["stock"][index]
            except Exception as e:
                print(f"Exception: {e}")
        with open("watchlist.json", "w") as jfile:
            jObj = json.dumps(data)
            jfile.write(jObj)

    def getDataframeFromStock(self, ticker):
        data = yf.download(ticker)
        data["daily_return"] = data["Adj Close"].pct_change()
        data["state"] = np.where(data["daily_return"] >= 0, "up", "down")
        return data

    def getAllPotentialTrades(self, minProbability):
        allPotentialTrades = []
        for ticker in self.tickers:
            allPotentialTrades += self.createMatricies(ticker, minProbability)
        pprint(allPotentialTrades)

    def dataframeMatrix(self, ticker):
        data = self.getDataframeFromStock(ticker)
        upToUp = len(data[(data["state"] == "up") & (data["state"].shift(-1) ==
                  "up")]) / len(data.query('state=="up"'))
        upToDown = len(data[(data["state"] == "down") & (data["state"].shift(-1)
                   == "up")]) / len(data.query('state=="up"'))
        downToDown = len(data[(data["state"] == "down") & (data["state"].shift(-
                  1) == "down")]) / len(data.query('state=="down"'))
        downToUp = len(data[(data["state"] == "up") & (data["state"].shift(-1) == "down")]) / len(data.query('state=="down"'))
        return pd.DataFrame({
                "up" : [upToUp, upToDown],
                "down" : [downToUp, downToDown]
                }, index=["up", "down"])


    def createFiveDayMatrix(self, ticker):
        data = self.getDataframeFromStock(ticker)
        downToUp5 = len(data[(data["state"].shift(-5) == "up")]) / len(data[(data["state"] == "down")
                    & (data["state"].shift(-1) == "down")
                    & (data["state"].shift(-2) == "down")
                    & (data["state"].shift(-3) == "down")
                    & (data["state"].shift(-4) == "down")
                    ])
        
        upToUp5 = len(data[(data["state"].shift(-5) == "up")]) / len(data[(data["state"] == "up") 
                           & (data["state"].shift(-1) == "up")
                           & (data["state"].shift(-2) == "up")
                           & (data["state"].shift(-3) == "up")
                           & (data["state"].shift(-4) == "up")
                           ])
        
        upToDown5 = len(data[(data["state"].shift(-5) == "down")]) / len(data[(data["state"] == "up") 
                             & (data["state"].shift(-1) == "up")
                             & (data["state"].shift(-2) == "up")
                             & (data["state"].shift(-3) == "up")
                             & (data["state"].shift(-4) == "up")
                             ])
        downToDown5 = len(data[(data["state"].shift(-5) == "down")]) /len(data[(data["state"] == "down") 
                               & (data["state"].shift(-1) == "down")
                               & (data["state"].shift(-2) == "down")
                               & (data["state"].shift(-3) == "down")
                               & (data["state"].shift(-4) == "down")
                               ])

        return pd.DataFrame({
                "up" : [upToUp5, upToDown5],
                "down" : [downToUp5, downToDown5] 
            }, index=["up", "down"])

    def createMatricies(self, ticker, minProbability):
        data = self.getDataframeFromStock(ticker)
        potentialTrades = []
        
        try:
            upToUp = len(data[(data["state"] == "up") & (data["state"].shift(-1) == "up")]) / len(data.query('state=="up"'))
            if upToUp >= minProbability:
                potentialTrades.append({
                    "ticker" : ticker,
                    "days" : 1,
                    "indicator" : "up",
                    "strategy" : "long",
                    "porbability" : upToUp
                })
        except:
            pass
        try:
            upToDown = len(data[(data["state"] == "down") & (data["state"].shift(-1) == "up")]) / len(data.query('state=="up"'))
            if upToDown >= minProbability:
                potentialTrades.append({
                    "ticker" : ticker,
                    "days" : 1,
                    "indicator" : "up",
                    "strategy" : "short",
                    "porbability" : upToDown
                })
        except:
            pass
        try:
            downToDown = len(data[(data["state"] == "down") & (data["state"].shift(-1) == "down")]) / len(data.query('state=="down"'))
            if downToDown >= minProbability:
                potentialTrades.append({
                    "ticker" : ticker,
                    "days" : 1,
                    "indicator" : "down",
                    "strategy" : "short",
                    "porbability" : downToDown
                })
        except:
            pass
        
        try:
            downToUp = len(data[(data["state"] == "up") & (data["state"].shift(-1) == "down")]) / len(data.query('state=="down"'))
            if downToUp >= minProbability:
                potentialTrades.append({
                    "ticker" : ticker,
                    "days" : 1,
                    "indicator" : "down",
                    "strategy" : "long",
                    "porbability" : downToUp
                })
        except:
            pass
        
        try:
            upToUp5 = len(data[(data["state"].shift(-5) == "up")]) / len(data[(data["state"] == "up") 
                           & (data["state"].shift(-1) == "up")
                           & (data["state"].shift(-2) == "up")
                           & (data["state"].shift(-3) == "up")
                           & (data["state"].shift(-4) == "up")
                           ])
            if upToUp5 >= minProbability:
                potentialTrades.append({
                    "ticker" : ticker,
                    "days" : 5,
                    "indicator" : "up",
                    "strategy" : "long",
                    "porbability" : upToUp5
                })
        except:
            pass
        try:
            upToDown5 = len(data[(data["state"].shift(-5) == "down")]) / len(data[(data["state"] == "up") 
                             & (data["state"].shift(-1) == "up")
                             & (data["state"].shift(-2) == "up")
                             & (data["state"].shift(-3) == "up")
                             & (data["state"].shift(-4) == "up")
                             ])
            if upToDown5 >= minProbability:
                potentialTrades.append({
                    "ticker" : ticker,
                    "days" : 5,
                    "indicator" : "up",
                    "strategy" : "short",
                    "porbability" : upToDown5
                })
        except:
            pass
        try:
            downToDown5 = len(data[(data["state"].shift(-5) == "down")]) /len(data[(data["state"] == "down") 
                               & (data["state"].shift(-1) == "down")
                               & (data["state"].shift(-2) == "down")
                               & (data["state"].shift(-3) == "down")
                               & (data["state"].shift(-4) == "down")
                               ])
        
            if downToDown5 >= minProbability:
                potentialTrades.append({
                    "ticker" : ticker,
                    "days" : 5,
                    "indicator" : "down",
                    "strategy" : "short",
                    "porbability" : downToDown5
                })
        except:
            pass
        try:
            downToUp5 = len(data[(data["state"].shift(-5) == "up")]) / len(data[(data["state"] == "down") 
                             & (data["state"].shift(-1) == "down")
                             & (data["state"].shift(-2) == "down")
                             & (data["state"].shift(-3) == "down")
                             & (data["state"].shift(-4) == "down")
                             ])
            if downToUp5 >= minProbability:
                potentialTrades.append({
                    "ticker" : ticker,
                    "days" : 5,
                    "indicator" : "down",
                    "strategy" : "long",
                    "porbability" : downToUp5
                })
        except:
            pass
        return potentialTrades
        
        
