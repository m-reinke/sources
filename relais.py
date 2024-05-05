import os
import board
import RPi.GPIO as gpio
import time
import datetime
import debug


######################################################################################
######################################################################################
######################################################################################

# Setting pin for sensor and optional switched senor power
# sensorpin = 12
# sensorpower = 26

# setting Output Pins
PFANU = 12  # Fan for internal airflow
PCOOL = 18  # cooling
PFANA = 23  # fan for air intake
PMOIS = 24  # ultrasonic moisturizer
PHEAT = 27  # heating

def initRelais():
    global PFANU
    global PCOOL
    global PFANA
    global PMOIS
    global PHEAT
    gpio.setwarnings(False)
    debug.debug_msg("Setting Board mode.....")
    gpio.setmode(gpio.BCM)
    debug.debug_msg("Setting up Outputs.....")
    gpio.setup(PFANU, gpio.OUT)
    gpio.setup(PCOOL, gpio.OUT)
    gpio.setup(PFANA, gpio.OUT)
    gpio.setup(PMOIS, gpio.OUT)
    gpio.setup(PHEAT, gpio.OUT)
    debug.debug_msg("Setting Outputs low.....")
    gpio.output(PFANU, gpio.LOW)
    gpio.output(PCOOL, gpio.LOW)
    gpio.output(PFANA, gpio.LOW)
    gpio.output(PMOIS, gpio.LOW)
    gpio.output(PHEAT, gpio.LOW)
        
def exitRelais():
    debug.debug_msg("Cleaning Up...")
    gpio.cleanup()
    debug.debug_msg("Cleanup complete!")

def set_states(data):

    if data.heat == 1:
        gpio.output(PHEAT, gpio.HIGH)
    else:
        gpio.output(PHEAT, gpio.LOW)
    if data.cool == 1:
        gpio.output(PCOOL, gpio.HIGH)
    else:
        gpio.output(PCOOL, gpio.LOW)
    if data.mois == 1:
        gpio.output(PMOIS, gpio.HIGH)
    else:
        gpio.output(PMOIS, gpio.LOW)
    if data.fana == 1:
        gpio.output(PFANA, gpio.HIGH)
    else:
        gpio.output(PFANA, gpio.LOW)
    if data.fanu == 1:
        gpio.output(PFANU, gpio.HIGH)
    else:
        gpio.output(PFANU, gpio.LOW)
