import threading
import db
import debug
import mysql.connector
from collections import deque
import climateconfig

class SqlWriter:

    def __init__(self):
        self.config = climateconfig.ClimateConfig()
        self.event = threading.Event()
        self.stopped = False
        self.queue = deque()
        self.thread = threading.Thread(target=self.run)        
        self.thread.start()        
        
    def push(self, data):    
        if self.stopped:
            debug.debug_msg("is stopped")
            return
    
        self.queue.append(data)
        count = len(self.queue)
        debug.debug_msg("Queue has %d entries" % count)
        self.event.set()
        self.event.clear()
        
    def stop(self):
        self.stopped = True
        self.event.set()
        self.thread.join()
            
    def mysql_write_archive(self, mydb, data):
        if self.config.logging != 1:
            return
            
        mycursor = mydb.cursor()
        sql = "INSERT INTO state_archive (timestamp, mode, temp, hum, heat, cool, moist, fan_a, fan_u, target_temp, target_hum) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (data.timestamp, data.mode, data.temp, data.hum, data.heat, data.cool, data.mois, data.fana, data.fanu, data.target_temp, data.target_hum)
        mycursor.execute(sql, val)
        mydb.commit()


    def mysql_set_current(self, mydb, data):
        mydb = db.getDb()
        mycursor = mydb.cursor()
        sql = "UPDATE state_current SET timestamp=%s, mode=%s, temp=%s, hum=%s, heat=%s, cool=%s, moist=%s, fan_a=%s, fan_u=%s WHERE id = 1"
        val = (data.timestamp, data.mode, data.temp, data.hum, data.heat, data.cool, data.mois, data.fana, data.fanu)
        mycursor.execute(sql, val)
        mydb.commit()


    def run(self):
        while not self.stopped:
            if self.config.load():
                self.writeSql()
            self.event.wait()
        debug.debug_msg("Exiting writer thread")

    def isEmpty(self):
        count = len(self.queue)
        if count == 0:
            debug.debug_msg("Queue empty")
            return True
        else:
            debug.debug_msg("Queue has %d" % count)
            return False
            
    def writeSql(self):
        debug.debug_msg("writing start")
        while not self.isEmpty():
            data = self.queue.pop()
            isEmpty = self.isEmpty()
            try:
                mydb = db.getDb()
                if isEmpty:
                    self.mysql_set_current(mydb, data)
                    
                self.mysql_write_archive(mydb, data)
            except Exception as error:
                print("Exception at writing to db:", error)
                self.queue.appendleft(data)
                return
        debug.debug_msg("writing ended")
                
        