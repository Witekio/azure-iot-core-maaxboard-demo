import os

MAPPINGS = {
    '7': {'gpio_reference': '80', 'status': 'OK'},
    '11': {'gpio_reference': '81', 'status': 'OK'},
    '22': {'gpio_reference': '79', 'status': 'OK'},
    '26': {'gpio_reference': '66', 'status': 'OK'},
    '29': {'gpio_reference': '69', 'status': 'OK'},
    '31': {'gpio_reference': '74', 'status': 'OK'},
    '32': {'gpio_reference': '15', 'status': 'OK'},
    '33': {'gpio_reference': '13', 'status': 'OK'},
    '36': {'gpio_reference': '3', 'status': 'OK'},
    '37': {'gpio_reference': '75', 'status': 'OK'},
}

PIN_NUMBER = input(f'Please enter one of these pin numbers for the GPIO you would like to use: {list(MAPPINGS.keys())}')

if PIN_NUMBER not in MAPPINGS.keys():
    print('Your *pin* number is not found, can you make sure you are using the PIN number not the GPIO?')

if PIN_NUMBER in MAPPINGS.keys():
    SYS_CLASS_NUMBER = MAPPINGS[PIN_NUMBER]['gpio_reference']
    print(f'Your pin number is {PIN_NUMBER}.\nThis corresponds to sys class number {SYS_CLASS_NUMBER}. Configuring this now.')
    os.system(f'echo {SYS_CLASS_NUMBER} > /sys/class/gpio/export')
    os.system(f'echo out > /sys/class/gpio/gpio{SYS_CLASS_NUMBER}/direction')
    print(f'Pin number {PIN_NUMBER} is now set up.')
    print('Please enter ON or OFF to turn the pin on or off. When finished, enter CLEAR to clear the pin.')
    while True:
        REQUEST = input('Enter ON, OFF, or CLEAR: ')
        if REQUEST == 'CLEAR':
            os.system(f'echo {SYS_CLASS_NUMBER} > /sys/class/gpio/unexport')
        if REQUEST == 'OFF': 
            os.system(f'echo 0 > /sys/class/gpio/gpio{SYS_CLASS_NUMBER}/value')
        if REQUEST == 'ON':
            os.system(f'echo 1 > /sys/class/gpio/gpio{SYS_CLASS_NUMBER}/value')
