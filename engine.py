
import time
class Barista:
    def __init__(self):
        self._id = None
        self.state = None
        self.name = None
        

    def makeDrink(self,drink = None):        
        # Make Drink
        self.state = 'busy'
        print ("worker " + str(self._id) + " is starting making  drink " + str(drink.order_id))        
        drink.brew()        
        print ("worker " + str(self._id) + " is done making  drink " + str(drink.order_id))
        self.state = 'free'



class Drink:
    def __init__(self):
        self.order_id = None
        self.order_time = None
        self.brew_time = None        
        self.type = None
        self.state = None                

    def brew(self):        
        time.sleep(self.order_time)
        