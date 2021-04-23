# iTracker


A set of scripts that allow you to collect and interpret information about your iPhone

While this project was made to be deployed on a Raspberry Pi, it can be used on OSX and Windows with little difficulty


# How to use tracker.py


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
The script above will give you a readout of your devices and their IDs

5. After running the script for the first time, if you have mfa enabled, you will have to authenticate via a code sent to one of your iDevices
6. While runnng, the script will give you data about your device every 300 seconds by default

On line 10, you can adjust the frequency at which the script will collect data about your device

On lines 12 through 16, you can indicate how and where to save the collected data

On lines 18 and 19, you can indicate if you want to be notified every time data is collected (this is only recommended if the data collection frequency is higher than 1500)
