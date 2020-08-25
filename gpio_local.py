#!/usr/bin/env python3

from pin import Pin, MAPPINGS, prompt_for_pin_number


if __name__ == "__main__":
    pin_number = prompt_for_pin_number()
    pin = Pin(pin_number)
    print(
        'Please enter ON or OFF to turn the pin on or off.'
    )
    while True:
        try: 
            REQUEST = input('Enter ON or OFF:')
            if REQUEST == 'OFF':
                pin.turn_off()
            if REQUEST == 'ON':
                pin.turn_on()
        finally:
            pin.tear_down()
