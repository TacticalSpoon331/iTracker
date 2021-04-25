# iTracker


A set of scripts that allow you to collect and interpret information about your iDevice through Find My services

While this project was made to be deployed on a Raspberry Pi, it can be used on OSX and Windows with little difficulty



# How to use tracker.py


This script will collect location and status data from an iDevice

1. Install pyicloud (https://pypi.org/project/pyicloud/) for python3
2. Put your AppleID credentials on lines 5 and 6 (These are only sent to Apple, they are not stored)
3. Put the desired device ID on line 8

```python
from pyicloud import PyiCloudService

APPLEID_EMAIL = 'PUT YOUR APPLE ID EMAIL HERE'
APPLEID_PASSWORD = 'PUT YOUR APPLE ID PASSWORD HERE'

iTracker = PyiCloudService(APPLEID_EMAIL, APPLEID_PASSWORD)

print(iTracker.devices)
```
The code above will give you a readout of your devices and their IDs

5. After running the script for the first time, if you have mfa enabled, you will have to authenticate via a code sent to one of your iDevices
6. While runnng, the script will give you data about your device every 300 seconds by default

On line 10, you can adjust the frequency at which the script will collect data about your device

On lines 12 through 16, you can indicate how and where to save the collected data

On lines 18 and 19, you can indicate if you want to be notified every time data is collected (this is only recommended if the data collection frequency is higher than 1500)



# How to use parser.py


This script will take csv data from tracker.py and sort it by location from most frequent in the dataset to least frequent

1. Get a reverse geocoding api key from https://positionstack.com
2. Put your api key on line 8
3. Specify the file that you want the script to read from on line 6
4. Uh... run the script and read the output with your eyeballs
