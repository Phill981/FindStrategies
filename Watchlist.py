import json
class Watchlist:
    def __init__(self) -> None:
        self.tickers = self._readWatchlist() 

    def _readWatchlist(self)->list[str]:
        with open("watchlist.json", "r") as jfile:
            data = json.load(jfile)
        return data["stock"]        
    
    def getTickers(self) ->list[str]:
        return self.tickers
    
    def addTickerToWatchlist(self, newTicker)->None:
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
    
    def removeTickerFromWatchlist(self, ticker)->None:
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
