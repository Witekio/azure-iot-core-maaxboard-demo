import os

# The sys GPIO references are obtained from: https://www.element14.com/community/groups/roadtest/blog/2020/04/20/maaxboard-roadtest-direct-gpio
# You can also directly calculate these by referencing the Pin configuration on page 22 here:
# https://www.avnet.com/opasdata/d120001/medias/docus/197/AES-MC-SBC-IMX8M-G-Hardware_UserManual-V1.0-EN.pdf?CMP=GL-Avnet-E14-cross-sell
# Then running it through this formula: 
# (x-1) * 32 + y
# Where x is the number right after GPIO in the "Signal Description" and y is the pin number. 
# For example, for Pin 7 we have a Signal Description of GPIO3_IO16
# To calculate the pin number we then have this when we plug the values into our formula:
# (3 - 1) * 32 + 16 = 80
# And another example for GPIO 11:
# We start with the signal description of GPIO3_IO17
# (x-1) * 32 + y 
# (3-1) * 32 + 17 = 81
# I've listed the mappings for these calculations below for common GPIOs

MAPPINGS = {
    '7': '80',
    '11': '81',
    '22': '79',
    '26': '66',
    '29': '69',
    '31': '74',
    '32': '15',
    '33': '13',
    '36': '3',
    '37': '75',
}

PIN_NUMBER = input(f'Please enter one of these pin numbers for the GPIO you would like to use: {list(MAPPINGS.keys())}')

if PIN_NUMBER not in MAPPINGS.keys():
    print('Your *pin* number is not found, can you make sure you are using the PIN number not the GPIO?')

if PIN_NUMBER in MAPPINGS.keys():
    SYS_CLASS_NUMBER = MAPPINGS[PIN_NUMBER]
    print(f'Your pin number is {PIN_NUMBER}.\nThis corresponds to sys class number {SYS_CLASS_NUMBER}. Configuring this now.')
    os.system(f'echo {SYS_CLASS_NUMBER} > /sys/class/gpio/export')
    os.system(f'echo out > /sys/class/gpio/gpio{SYS_CLASS_NUMBER}/direction')
    print(f'Pin number {PIN_NUMBER} is now set up.')
    print('Please enter ON or OFF to turn the pin on or off. When finished, enter CLEAR to clear the pin.')
    while True:
        REQUEST = input('Enter ON, OFF, or CLEAR: ')
        if REQUEST == 'CLEAR':
            os.system(f'echo {SYS_CLASS_NUMBER} > /sys/class/gpio/unexport')
            break
        if REQUEST == 'OFF': 
            os.system(f'echo 0 > /sys/class/gpio/gpio{SYS_CLASS_NUMBER}/value')
        if REQUEST == 'ON':
            os.system(f'echo 1 > /sys/class/gpio/gpio{SYS_CLASS_NUMBER}/value')
