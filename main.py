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

    def worker(self,barista):
        # workers will work until list of orders is empty after that they die
        print (str(barista._id) + " is working" )
        # get the a drink
        
        while(True):    
            if len(self.pending_orders_queue) <= 0:
                break

            for order in self.pending_orders_queue:
                if order.state == "done":
                    continue
                else:
                    tmpore = order
                    self.pending_orders_queue.remove(order)
                    barista.makeDrink(tmpore)                
                    self.done_orders_queue.append(tmpore)                    
                    break


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
            tmpdrink.state = "pending" # using simple text just for demo
            self.pending_orders_queue.append(tmpdrink)
            
        # create the workers they will select the drinks based on the order time (asc) and state, once is brew they will change the state to done, preferly to putting on another queeue of donde orders
        for b in self.baristas:
            barista = Barista()
            barista._id = b['id']
            t = threading.Thread(target=self.worker,args=(barista,))
            self.threads.append({'index':b['id'],'thread':t})
            t.start()              
            
        


if __name__ == "__main__":
    shop = Shop()
    shop.openConfig()
    shop.OpenStore()
        

