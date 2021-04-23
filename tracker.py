import json, time, os
from datetime import datetime
from pyicloud import PyiCloudService

APPLEID_EMAIL = 'PUT YOUR APPLE ID EMAIL HERE'
APPLEID_PASSWORD = 'PUT YOUR APPLE ID PASSWORD HERE'

TARGET_DEVICE_ID = 'PUT THE TARGET DEVICE ID HERE' # Get device IDs via iTracker.devices

data_collection_frequency = 300 # seconds

save_data_csv = True
csv_data_filename = 'location_data.csv'

save_data_json = True
json_data_filename = 'location_data.json'

notify_when_data_collected = True
notification_message = f'''iTracker Alert:
	Status Data Collected'''


iTracker = PyiCloudService(APPLEID_EMAIL, APPLEID_PASSWORD)

def checkMFA():

	if iTracker.requires_2fa:
	    print("Two-factor authentication required.")
	    code = input("Enter the code you received of one of your approved devices: ")
	    result = iTracker.validate_2fa_code(code)
	    print("Code validation result: %s" % result)

	    if not result:
	        print("Failed to verify security code")
	        sys.exit(1)

	    if not iTracker.is_trusted_session:
	        print("Session is not trusted. Requesting trust...")
	        result = iTracker.trust_session()
	        print("Session trust result %s" % result)

	        if not result:
	            print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
	elif iTracker.requires_2sa:
	    import click
	    print("Two-step authentication required. Your trusted devices are:")

	    devices = iTracker.trusted_devices
	    for i, device in enumerate(devices):
	        print("  %s: %s" % (i, device.get('deviceName',
	                    "SMS to %s" % device.get('phoneNumber'))))

	    device = click.prompt('Which device would you like to use?', default=0)
	    device = devices[device]
	    if not iTracker.send_verification_code(device):
	        print("Failed to send verification code")
	        sys.exit(1)

	    code = click.prompt('Please enter validation code')
	    if not iTracker.validate_verification_code(device, code):
	        print("Failed to verify verification code")
	        sys.exit(1)



def getDeviceData(ID):

	timeStamp = (iTracker.devices[ID].location()['timeStamp'])
	timeStamp = datetime.fromtimestamp(timeStamp * 1e-3)

	latitude = (iTracker.devices[ID].location()['latitude'])
	longitude = (iTracker.devices[ID].location()['longitude'])

	altitude = (iTracker.devices[ID].location()['altitude'])
	floorLevel = (iTracker.devices[ID].location()['floorLevel'])
	positionType = (iTracker.devices[ID].location()['positionType'])

	batteryLevel = round((iTracker.devices[ID].status()['batteryLevel']) * 100)

	deviceModel = (iTracker.devices[ID].status()['deviceDisplayName'])
	deviceName = (iTracker.devices[ID].status()['name'])

	saveData(timeStamp, latitude, longitude, altitude, floorLevel, positionType, batteryLevel, deviceModel, deviceName)


	print('====================================')
	print(f'Time: {timeStamp}')
	# print('\n')
	print(f'Latitude: {latitude}')
	print(f'Longitude: {longitude}')
	print(f'Altitude: {altitude} ft')
	print(f'Estimated floor level: {floorLevel}')
	print(f'Location data gathered via: {positionType}')
	# print('\n')
	print(f'{batteryLevel}% battery life remaining')
	# print('\n')
	print(f'Device model: {deviceModel}')
	print(f'Device name: {deviceName}')
	print('====================================')

	print('\n\n')




def saveData(timeStamp, latitude, longitude, altitude, floorLevel, positionType, batteryLevel, deviceModel, deviceName):

	if save_data_csv == True:

		f = open(csv_data_filename, "a")
		f.write(f'{timeStamp},{deviceName},{positionType},{latitude},{longitude},{altitude} ft,Floor {floorLevel},{batteryLevel}%')
		f.write('\n')
		f.close()

	json_output = {"Time": f"{timeStamp}","Latitude": f"{latitude}","Longitude": f"{longitude}","Altitude": f"{altitude}","Estimated floor level": f"{floorLevel}","Method for location data collection": f"{positionType}","Battery life remaining": f"{batteryLevel}%","Device model": f"{deviceModel}","Device name": f"{deviceName}"}
	json_output = json.dumps(json_output, indent=4)

	if save_data_json == True:


		f = open(json_data_filename, "a")
		f.write(json_output)
		f.write('\n')
		f.close()

	if notify_when_data_collected == True:

		iTracker.devices[TARGET_DEVICE_ID].display_message('', f'''{notification_message}
	{json_output}''', False)


checkMFA()

while True:
	getDeviceData(TARGET_DEVICE_ID)
	time.sleep(data_collection_frequency)
