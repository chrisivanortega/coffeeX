from engine import Barista,Drink

class Shop:
    def __init__(self):
        self.shift = 100
        # a db would be better 
        self.drinks =  [
            { "type": "tea",      "brew_time": 3, "profit": 2 },
            { "type": "latte",    "brew_time": 4, "profit": 3 },
            { "type": "affogato", "brew_time": 7, "profit": 5 }
        ]
        self.baristas = [
            {"id":1,"name":"John"},
            {"id":2,"name":"Peter"}
        ]

if __name__ == "__main__":
    shop = Shop()
        

