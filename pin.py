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


class Pin:
    def __init__(self, pin_number):
        self.pin_number = str(pin_number)
        self.sys_pin_number = MAPPINGS[self.pin_number]
        print(f'Your pin number is {self.pin_number}.\n')
        print(f'Your system gpio number is {self.sys_pin_number}.\n')
        
    def turn_on(self):
        os.system(f'echo 1 > /sys/class/gpio/gpio{self.sys_pin_number}/value')

    def turn_off(self):
        os.system(f'echo 0 > /sys/class/gpio/gpio{self.sys_pin_number}/value')

    def configure(self):
        os.system(f'echo {self.sys_pin_number} > /sys/class/gpio/export')
        os.system(f'echo out > /sys/class/gpio/gpio{self.sys_pin_number}/direction')

    def tear_down(self):
        os.system(f'echo {self.sys_pin_number} > /sys/class/gpio/unexport')
   