import os
import time
from pin import Pin
from azure.iot.device import IoTHubDeviceClient

conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

PIN_NUMBER = input(
    'Please enter one of these pin numbers for the GPIO '
    f'you would like to use: {list(MAPPINGS.keys())}'
)
configured_pin = Pin(PIN_NUMBER)

# Connect the IoTHub client
device_client.connect()

# Get the device twin document
twin = device_client.get_twin()
print("Initial twin document:")
print("{}".format(twin))


def report_light_state(state):
    reported_properties = {"light": state}
    light_state = reported_properties["light"]
    print(f"Setting reported light state to {light_state}")
    device_client.patch_twin_reported_properties(reported_properties)


# Initalize the light as off in reported properties:
report_light_state("OFF")


while True:
    request = input('Enter ON, OFF, LISTEN, or CLEAR: ')
    if request == "CLEAR":
        configured_pin.tear_down()
        report_light_state("OFF")
        device_client.disconnect()
        break
    if request == "OFF":
        configured_pin.turn_off()
        report_light_state("OFF")
    if request == "ON":
        configured_pin.turn_on()
        report_light_state("ON")
    if request == 'LISTEN':
        last_desired_light_state = ''
        while True:
            twin = device_client.get_twin()
            if not twin['desired'].get('light'):
                print('No desired light property set')
                break
            desired_light_state = twin['desired']['light']
            if last_desired_light_state != desired_light_state:
                if desired_light_state == 'OFF':
                    configured_pin.turn_off()
                    report_light_state(desired_light_state)
                    last_desired_light_state = desired_light_state
                if desired_light_state == 'ON':
                    configured_pin.turn_on()
                    report_light_state(desired_light_state)
                    last_desired_light_state = desired_light_state
            else:
                print('No update to desired light state detected')
            time.sleep(3)
