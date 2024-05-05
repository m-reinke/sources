import os
import debug
import board
import adafruit_htu31d
import time
import datetime


class ClimateData:
	def __init__(self):
		ts = time.time()
		self.timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		self.temp = 0
		self.hum = 0
		self.cool = 0
		self.heat = 0
		self.mois = 0
		self.fana = 0
		self.fanu = 1
		self.target_temp = 0
		self.target_hum = 0
		self.mode = 0
		# Sensor should be set to Adafruit_DHT.DHT22
		self.i2c = board.I2C()
		self.sensor = adafruit_htu31d.HTU31D(self.i2c)
		debug.debug_msg("HTU31D serial number {0} ".format(hex(self.sensor.serial_number)))

		
	def read_sensor(self):
		# setting up array for median filter
		hum = [1,2,3,4,5,6,7,8]
		temp = [1,2,3,4,5,6,7,8]

		# read sensor data and getting 8 values
		for x in range(8):
			temperature, humidity = self.sensor.measurements
			if humidity is not None and temperature is not None:
				# debug.debug_msg('Reading {0} Temp={1:0.1f}*C  Humidity={2:0.1f}%'.format(x, temperature, humidity))
				hum[x]=humidity
				temp[x]=temperature
			else:
				debug.debug_msg('No reading')
		# sort Arrays
		hum.sort()
		temp.sort()

		# printing values and using median filter
		debug.debug_msg('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temp[4], hum[4]))
		self.temp = temp[4]
		self.hum = hum[4]
		
			
	def evaluate(self, config):
		debug.debug_msg("starting control... Mode(1): self.cool, self.heat, self.moist, self.fana ")

		self.target_temp = config.temp
		self.target_hum = config.hum
		self.mode = config.mode
		
		if self.temp > config.temp + config.temp_hyst_cool:
			self.cool = 1
			self.fanu = 1
		else:
			self.cool = 0
		if self.temp < config.temp - config.temp_hyst_heat:
			self.heat = 1
			self.fanu = 1
		else:
			self.heat = 0
		if self.hum > config.hum + config.hum_hyst_fana:
			self.fana = 1
			self.fanu = 1
		else:
			self.fana = 0
		if self.hum < config.hum - config.hum_hyst_mois:
			self.mois = 1
			self.fanu = 1
		else:
			self.mois = 0
		if self.cool == 1 or self.heat == 1 or self.mois == 1 or self.fana == 1:
			self.fanu = 1
		else:
			self.fanu = 0
		
		
		
	def print_status(self, config):
		os.system('clear')
		print ("######################################")
		print ("Soll Temperatur: {} *C".format(config.temp))
		print ("Ist- Temperatur: {:.1f} *C".format(self.temp))
		print ("######################################")
		print ("Soll Luftfeuchte: {} %Lf".format(config.hum))
		print ("Ist- Luftfeuchte: {:.1f} %Lf".format(self.hum))
		print ("######################################")
		print ("Kuehlung:     {} an bei: {} *C".format(self.cool,config.temp + config.temp_hyst_cool))
		print ("Heizung:      {} an bei: {} *C".format(self.heat,config.temp - config.temp_hyst_heat))
		print ("Befeuchtung:  {} an bei: {} %Lf".format(self.mois,config.hum - config.hum_hyst_mois))
		print ("Luftaustausch:{} an bei: {} %Lf".format(self.fana,config.hum + config.hum_hyst_fana))
		print ("Umluft:       {}".format(self.fanu))
		print ("Reading:      {}".format(self.timestamp))
		print ("######################################")
	