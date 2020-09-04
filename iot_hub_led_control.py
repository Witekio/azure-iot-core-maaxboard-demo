#!/usr/bin/env python3

import os
import time
from pin import Pin, prompt_for_pin_number
from azure.iot.device import IoTHubDeviceClient

conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")


def create_iot_hub_device_client():
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
    device_client.connect()
    twin = device_client.get_twin()
    print("Initial twin document:\n")
    print("{}".format(twin))
    return device_client


def report_light_state(state, device_client):
    reported_properties = {"light": state}
    light_state = reported_properties["light"]
    print(f"Setting reported light state to {light_state}")
    device_client.patch_twin_reported_properties(reported_properties)


def listen(device_client, configured_pin):
    last_desired_light_state = ''
    while True:
        twin = device_client.get_twin()
        if not twin['desired'].get('light'):
            print('No desired light property set')
            break
        desired_light_state = twin['desired']['light']
        if desired_light_state != last_desired_light_state:
            if desired_light_state == 'OFF':
                configured_pin.turn_off()
                report_light_state(desired_light_state, device_client)
                last_desired_light_state = desired_light_state
            if desired_light_state == 'ON':
                configured_pin.turn_on()
                report_light_state(desired_light_state, device_client)
                last_desired_light_state = desired_light_state
        else:
            print('No update to desired light state detected')
        time.sleep(3)


if __name__ == "__main__":
    try:
        device_client = create_iot_hub_device_client()
        # Initalize the light as OFF in reported properties
        report_light_state("OFF", device_client)
        pin_number = prompt_for_pin_number()
        configured_pin = Pin(pin_number)
        while True:
            request = input('Enter ON, OFF, or LISTEN: ')
            if request == "OFF":
                configured_pin.turn_off()
                report_light_state("OFF", device_client)
            if request == "ON":
                configured_pin.turn_on()
                report_light_state("ON", device_client)
            if request == 'LISTEN':
                listen(device_client, configured_pin)
    finally:
        configured_pin.tear_down()
        report_light_state("OFF", device_client)
        device_client.disconnect()
