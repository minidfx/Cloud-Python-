import os
import sys

from Amazon import Amazon
from OpenStack import OpenStack

if sys.version_info.major < 2 and sys.version_info.minor < 7:
    raise Exception("Python version 2.7 minimum is required for running this script.")

clouds = [OpenStack(), Amazon()]

for cloud in clouds:
    cloud.create()

print('Press \'A\' to destroy instances created.')

consoleInput = os.read(0, 1)

while consoleInput != b'A':
    consoleInput = os.read(0, 1)

for cloud in clouds:
    cloud.destroy()

print("Delivrable terminated.")
