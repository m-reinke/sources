
import mysql.connector

def getDb():
    return mysql.connector.connect(host="nas", user="reifeschrank", passwd="HMlj-14879", database="reifeschrank")
