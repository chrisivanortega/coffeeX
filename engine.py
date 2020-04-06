
class Barista:
    def __init__(self):
        self._id = None
        self.state = None
        self.name = None

    def makeDrink(self,drinkId):
        # Make Drink 
        return results

class Drink:
    def __init__(self):
        self._id = None
        self.name = None
        self.execTime = None
        self.price = None
        self.priority = None

    def makeMe(self):
        import time
        try:
            self.execTime
        except Exception as e:
            self.execTime = 60
        # we can put it to sleep, but i like to simulate some cpu time to check performance
        for i in range(1, self.execTime):
            self.execTime / self.execTime * 2
            time.sleep(1)  