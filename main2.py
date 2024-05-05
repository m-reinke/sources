
import climatedata
import climateconfig
import db
import sqlwriter
import relais
import debug
import time


config = climateconfig.ClimateConfig()
sqlwriter = sqlwriter.SqlWriter()

refreshrate = 10

def main_loop():
    global config
    global sqlwriter
    global refreshrate

    try:
        while config.power == 1:
            config.load("main")        

            data = climatedata.ClimateData()
            data.read_sensor()
            data.evaluate(config)
            data.print_status(config)
            
            relais.set_states(data)
            sqlwriter.push(data)            

            debug.debug_msg("Waiting for delay")
            time.sleep(refreshrate)
    except KeyboardInterrupt:
        pass
    

relais.initRelais()
config.load()
if config.power == 0:
    debug.debug_msg("Power in webinterface is switched off....")

if config.power == 1:
    main_loop()

sqlwriter.stop()
relais.exitRelais()
