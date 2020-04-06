
import time
class Barista:
    def __init__(self):
        self._id = None
        self.state = None
        self.name = None
        self.start_time = None
        self.last_brew_time = None
        self.last_order_time = None
        self.orders_taken = None

        
    def toString(self):
        return {"id":self._id,"last_brew_time":self.last_brew_time,"last_order_time":self.last_order_time}

    def makeDrink(self,drink = None):        
        # Make Drink
        self.state = 'busy'
        #print ("worker " + str(self._id) + " is starting making  drink " + str(drink.order_id))        
        drink.brew()        
        #print ("worker " + str(self._id) + " is done making  drink " + str(drink.order_id))
        self.state = 'free'


class Drink:
    def __init__(self):
        self.order_id = None
        self.order_time = None
        self.brew_time = None        
        self.type = None
        self.state = None                

    def toString(self):
        return {"id":self.order_id,"order_time":self.order_time,"brew_time":self.brew_time,"type":self.type}

    def brew(self):        
        time.sleep(self.brew_time)
        return
        
