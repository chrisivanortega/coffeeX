from engine import Barista,Drink
import os

import json
import sys

import threading
import time

import random 
class Shop:
    def __init__(self):
        self.shift = 100
        self.start_shift = 0
        self.counter_shift = 0
        # a db would be better 
        self.drinks =  [
            { "type": "tea",      "brew_time": 3, "profit": 2 },
            { "type": "latte",    "brew_time": 4, "profit": 3 },
            { "type": "affogato", "brew_time": 7, "profit": 5 }
        ]
        self.baristas = [
            {"id":1},
            {"id":2}
        ]        
        self.config = None

        self.threads = []
        self.tindex = 0
        self.pool = []     

        self.pending_orders_queue = []
        self.done_orders_queue = []
        self.free_baristas = []
        self.busy_baristas = []

    def openConfig(self):                
        try:
            f = open("config.json", "r")
            self.config = json.loads(f.read())        
        except Exception as e:
            print ("error 1: config error =  " + str(e))
            sys.exit(0)

    def getOrders(self):
        try:            
            return self.config['orders']
        except Exception as e:
            print ("error 2: config error =  " + str(e))
            sys.exit(0)            

    def worker(self,barista,order):
        # workers will work until list of orders is empty after that they die        
        # get the a drink
        #barista.makeDrink(order)
        #self.pending_orders_queue.remove(order)
        r1 = random.randint(0, 2) 
        
        print ("worker " +  str(barista._id) + " procees time " + str(r1))
        
        time.sleep(r1)        
        barista.state = 'free'
        self.free_baristas.append(barista)
        return None



    def OpenStore(self):
        # get orders
        # create the queue of orders so workers can get roders work on them until they are empty, if a new order comes triug it must be added to the queue
        self.pending_orders_queue = []
        self.done_orders_queue = []
        orders = self.getOrders()
        # order by order time
        orders = sorted(orders, key = lambda i: i['order_time']) 
        
        for order in orders:
            tmpdrink = Drink()
            tmpdrink.order_id = order['order_id']
            tmpdrink.order_time = order['order_time']
            tmpdrink.type = order['type']
            tmpdrink.state = "pending" 
            self.pending_orders_queue.append(tmpdrink)
            
        # create the workers they will select the drinks based on the order time (asc) and state, once is brew they will change the state to done, preferly to putting on another queeue of donde orders
        for b in self.baristas:
            barista = Barista()
            barista._id = b['id']
            barista.state = 'free'
            self.free_baristas.append(barista)

        
        while(True):
            self.counter_shift+1
            if len(self.pending_orders_queue) <= 0  or self.counter_shift == self.shift:                
                break
     
            for barista in self.free_baristas:
                if barista.state == 'free':
                    self.free_baristas.remove(barista) 
                    print ("start worker")                                   
                    t = threading.Thread(target=self.worker,args=(barista,order))                    
                    t.start()              
            
        

if __name__ == "__main__":
    shop = Shop()
    shop.openConfig()
    shop.OpenStore()
        

