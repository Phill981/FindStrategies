import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
from pandas import DataFrame

class TransitionStates:
    def _getCall(self, data:DataFrame)->str:
        lastThreeDays = data.head(3)["state"].to_list()
        if(len(lastThreeDays) > 0):
            if(lastThreeDays[0] == lastThreeDays[1] and
               lastThreeDays[1] == lastThreeDays[2]):
                if(lastThreeDays[0] == "up"):
                    return "short"
                if(lastThreeDays[0] == "down"):
                    return "long"
        return "no call"
    
    def calculate_average_movement(self, 
            data:DataFrame, 
            start_index:int, 
            end_index:int)->float:
        movements = [data['Close'][i] - data['Open'][i] for i in range(start_index, end_index + 1)]
        return sum(movements) / len(movements)
    
    def _calcAvgMov(self, data:DataFrame, movement:str):
        consecutive_days = 3
        total_up_movement = 0.0
        total_down_movement = 0.0
        consecutive_positive_days = 0
        consecutive_negative_days = 0

        for i in range(1, len(data)):
            if data['Close'][i] > data['Close'][i - 1]:
                consecutive_positive_days += 1
                consecutive_negative_days = 0
            elif data['Close'][i] < data['Close'][i - 1]:
                consecutive_negative_days += 1
                consecutive_positive_days = 0
            else:
                consecutive_negative_days = 0
                consecutive_positive_days = 0

            if consecutive_positive_days == consecutive_days:
                total_up_movement += self.calculate_average_movement(
                    data, 
                    i - consecutive_days + 1,
                    i)
                consecutive_positive_days = 0

            elif consecutive_negative_days == consecutive_days:
                total_down_movement += self.calculate_average_movement(
                    data, 
                    i - consecutive_days + 1,
                    i)
                consecutive_negative_days = 0

        if movement == "up":
            average_up_movement = total_up_movement / (len(data) - consecutive_days)
            return average_up_movement
        elif movement == "down":
            average_down_movement = total_down_movement / (len(data) - consecutive_days)
            return average_down_movement
        else:
            return 0.0
        
        
    def formatTodaysDate(self)->str:

        today_date = datetime.now().strftime("%Y-%m-%d")
        return today_date
    
    def formatEarlierDate(self, yearsBack:int)->str:
        
        today_date = datetime.now()
        three_years_ago_date = today_date - timedelta(days=yearsBack * 365)
        formatted_date = three_years_ago_date.strftime("%Y-%m-%d")
        return formatted_date

                         
    def _formatDataFrame(self, data:DataFrame)->DataFrame:
        data["daily_return"] = data["Adj Close"].pct_change()
        data["state"] = np.where(data["daily_return"] >= 0, "up", "down")
        return data
    
    def _get_current_price(self, ticker:str)->float:
        stock = yf.download(ticker, progress=False)
        current_price = stock["Close"].to_list()[-1]
        return current_price       
        
    def _calculateTransitionMatrecies(self, data:DataFrame)->list[float]:
        upToDown = (
            len(data[(data["state"] == "down") & (data["state"].shift(-1) == "up") & (data["state"].shift(-2) == "up")& (data["state"].shift(-3) == "up")]) /
            len(data[(data["state"].shift(1) == "up") & (data["state"].shift(2) == "up")& (data["state"].shift(3) == "up")]) 
            )
        
        downToUp = (
            len(data[(data["state"] == "up") & (data["state"].shift(-1) == "down") & (data["state"].shift(-2) == "down")& (data["state"].shift(-3) == "down")]) /
            len(data[(data["state"].shift(1) == "down") & (data["state"].shift(2) == "down")& (data["state"].shift(3) == "down")]) 
            )
        return [upToDown, downToUp]
    
    def _calculateStd(self, data: DataFrame)->float:
        std = np.std(data["Close"].to_list())
        return std
    
    def _calculatePriceGoal(self, 
            std:float, 
            currentPrice:float, 
            avgMovement:float, 
            movement:str="")->list[float]:
        if movement == "down":
            return [
                currentPrice - (avgMovement * std),
                currentPrice * (1 - avgMovement)
                ]
        else:
            return [
                currentPrice + (avgMovement * std),
                currentPrice * (1 + avgMovement)
                ]
    
    def _analyze(self, data: DataFrame, ticker:str, move:str)->dict:
        
        call = self._getCall(data)
        transitionMatrecies = self._calculateTransitionMatrecies(data)
        
        averageMovement = self._calcAvgMov(data, move)
        std = self._calculateStd(data)
        currentPrice = self._get_current_price(ticker)
        priceGoal = self._calculatePriceGoal(std, currentPrice, averageMovement, move)
        
        if(transitionMatrecies[0] > 0):
            return {
                "status" : True,
                "ticker" : ticker,
                "call" : call,
                "price goal" : round(priceGoal[0], 2),
                #"price goal AVG" : round(priceGoal[1], 2),
                "current price" : round(currentPrice, 2),
                "probability" : transitionMatrecies[0] 
                    if call == "short" else transitionMatrecies[1]
            }
        else:
            return {"status" : False}
        
    
    def startStrategy(self, ticker:str)->dict:
        # Variable to determine how long ago the data should be grabbed from. 
        # Decided on three so avg values do not differ to much.
        yearsBackData:int = 3
        
        data = yf.download(
            ticker, 
            start=self.formatEarlierDate(yearsBackData), 
            end=self.formatTodaysDate(), 
            progress=False)
        data = self._formatDataFrame(data)
        
        lastThreeDays = data.head(3)["state"].to_list()
        if(len(lastThreeDays) > 0):
            if(lastThreeDays[0] == lastThreeDays[1] and
               lastThreeDays[1] == lastThreeDays[2]):
                movement = "up" if lastThreeDays[0] == "down" else "down"
                return self._analyze(data, ticker, movement)
            else:
                return {"status" : False}
        else:
            return {"status" : False}
