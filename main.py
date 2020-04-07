from engine import Barista,Drink
import os
import json
import sys
import threading
import time
import sys


class Shop:
    def __init__(self):
        self.shift = 100
        self.start_shift = 0
        self.counter_shift = 0
        

        self.drinks =  {
            "tea":{"brew_time": 3, "profit": 2 },
            "latte":{"brew_time": 4, "profit": 3 },
            "affogato":{"brew_time": 7, "profit": 5 }            
        }

        self.baristas = [
            {"id":1},
            {"id":2}            
        ]        

        self.config = None                         
        self.pending_orders_queue = []        
        self.free_baristas = []
        self.manager_report = []
        
        
    # opne config file
    def openConfig(self):                
        try:
            f = open("config.json", "r")
            self.config = json.loads(f.read())        
        except Exception as e:
            print ("error 1: config error =  " + str(e))
            sys.exit(0)

    # get the orders from the config file
    def getOrders(self):
        try:            
            return self.config['orders']
        except Exception as e:
            print ("error 2: config error =  " + str(e))
            sys.exit(0)            

    def worker(self,barista,order):   
        # worker that works independently on threads   
        barista.state = 'busy'
        barista.makeDrink(order)           
        if barista.last_order_time == 0:
            barista.last_order_time = order.order_time
        start_time = barista.last_order_time + barista.last_brew_time
        barista.last_order_time = start_time
        barista.last_brew_time = order.brew_time
        
        report  = {
            "barista_id": barista._id,
            "start_time":start_time,
            "order_id": order.order_id
        }   
        
        self.free_baristas.append(barista)         
        self.manager_report.append(report)
        barista.state = 'free'                                                        
        # no need to return values all is saved to the report
        # once the work is done the thread die
        
        

    def manager(self,orders = []):
        # creating the orders objects
        pending_orders_queue = []
        for order in orders:
            tmpdrink = Drink()
            tmpdrink.order_id = order['order_id']
            tmpdrink.order_time = order['order_time']
            tmpdrink.type = order['type']
            
            tmpdrink.brew_time = self.drinks[order['type']]['brew_time']
            tmpdrink.state = "pending" 
            pending_orders_queue.append(tmpdrink)
            
        # create the workers they will select the drinks based on the order time (asc) and state, once is brew they will change the state to done, preferly to putting on another queeue of donde orders
        for b in self.baristas:
            barista = Barista()
            barista._id = b['id']
            barista.state = 'free'
            barista.start_time = 0
            barista.last_brew_time = 0
            barista.orders_taken = 0
            barista.last_order_time = 0
            self.free_baristas.append(barista)

        # loop until all orders are made
        while(True):            
            if len(self.manager_report) == len(orders)  or self.counter_shift == self.shift:                
                break
            # we are going to loop throgh the free baristas, those who are busy we are jumping them
            for barista in self.free_baristas:                
                if barista.state == 'free':
                    self.free_baristas.remove(barista)
                    try:
                        # we are removing the order from the list
                        order = pending_orders_queue[0]
                        pending_orders_queue.remove(order)                        
                    except Exception as e:                        
                        continue                                 
                    # creating a trhead so baristas can multitask       
                    t = threading.Thread(target=self.worker,args=(barista,order))                    
                    t.start()

        return (json.dumps(shop.manager_report))


    def OpenStoreFIFO(self):
        orders = self.getOrders()        
        #NO ORDER FOR FIFO              
        return self.manager(orders)


    def OpenStoreTIME(self):
        orders = self.getOrders()        
        # ORDER BY TIME OF BREW TIME FOR BETTER CS
        for order in orders:
            order['brew_time'] =  self.drinks[order['type']]['brew_time']        
        orders = sorted(orders, key = lambda i: i['brew_time'])                 
        return self.manager(orders)            

    def OpenStorePROFFIT(self):
        orders = self.getOrders()
        for order in orders:
            order['profit'] =  self.drinks[order['type']]['profit']
        orders = sorted(orders, key = lambda i: i['profit'],reverse=True)                 
        return self.manager(orders)              
        # ORDER BY type OF BREW TIME FOR BETTER PROFFIT
        #orders = sorted(orders, key = lambda i: i['order_time'])       
     
         
        
if __name__ == "__main__":
    
    
    while(True):
        var = input("Welcome select a service method: \n 1- FIFO \n 2- TIME \n 3- PROFIT \n any other key- exit \n  ")
        if var in ["1"]:
            shop = Shop()
            shop.openConfig()
            data = shop.OpenStoreFIFO()   
            print (data)
        if var in ["2"]:
            shop = Shop()
            shop.openConfig()
            data = shop.OpenStoreTIME()   
            print (data)    
        if var in ["3"]:
            shop = Shop()
            shop.openConfig()
            data = shop.OpenStorePROFFIT()   
            print (data)                    
        if var not in ["1","2","3"]:
            break            

    print ("Good Bye!")
    


    
        
