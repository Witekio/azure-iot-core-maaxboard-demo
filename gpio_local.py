import os
from pin import Pin, MAPPINGS

PIN_NUMBER = input(f'Please enter one of these pin numbers for the GPIO you would like to use: {list(MAPPINGS.keys())}')

if PIN_NUMBER not in MAPPINGS.keys():
    print('Your *pin* number is not found, can you make sure you are using the PIN number not the GPIO?')

if PIN_NUMBER in MAPPINGS.keys():
    pin = Pin(PIN_NUMBER)
    pin.configure()
    print('Please enter ON or OFF to turn the pin on or off. When finished, enter CLEAR to clear the pin.')
    while True:
        REQUEST = input('Enter ON, OFF, or CLEAR: ')
        if REQUEST == 'CLEAR':
            pin.tear_down()
            break
        if REQUEST == 'OFF': 
            pin.turn_off()
        if REQUEST == 'ON':
            pin.turn_on()
