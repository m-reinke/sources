import db
import debug

class ClimateConfig:

#	def __init__(self, power, logging, mode, temp, hum, hum_hyst_mois, hum_hyst_fana, temp_hyst_cool, temp_hyst_heat)
#		self.power = power
#		self.logging = logging
#		self.mode = mode
#		self.temp = temp 
#		self.hum = hum  
#		self.hum_hyst_mois = hum_hyst_mois 
#		self.hum_hyst_fana = hum_hyst_fana 
#		self.temp_hyst_cool = temp_hyst_cool
#		self.temp_hyst_heat = temp_hyst_heat	
		
	def __init__(self):
		self.power = 0
		self.logging = 0
		self.mode = 0
		self.temp = 0 
		self.hum = 0  
		self.hum_hyst_mois = 0 
		self.hum_hyst_fana = 0 
		self.temp_hyst_cool = 0
		self.temp_hyst_heat = 0
		
	def load(self, context = ""):		
		#debug.debug_msg("reading config %s".format(context))
		try:

			myDb = db.getDb()
			mycursor = myDb.cursor()
			mycursor.execute("SELECT * FROM config_current")
			myresult = mycursor.fetchall()
			for row in myresult:
				currentglobal = row

		except Exception as error:
			print("%s Error loading config: %s" % (error, context))
			return False


		self.power = currentglobal[1]
		self.logging = currentglobal[2]
		self.mode = currentglobal[3]
		self.temp = currentglobal[4]
		self.hum = currentglobal[5]
		self.hum_hyst_mois = currentglobal[6]
		self.temp_hyst_cool = currentglobal[7]
		self.hum_hyst_fana = currentglobal[8]
		self.temp_hyst_heat = currentglobal[9]

		debug.debug_msg("Power: %d" % self.power)
		return True

		