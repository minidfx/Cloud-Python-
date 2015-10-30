from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

from settings import *


class Amazon:
    def __init__(self):
        amazon = get_driver(Provider.EC2_EU_WEST)
        self.driver = amazon(accessKey, secretKey)

    def create(self):
        raise Exception("Not implemented")

    def destroy(self):
        raise Exception("Not implemented")
