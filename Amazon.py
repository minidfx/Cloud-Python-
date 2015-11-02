# Getting started with OpenStack using libcloud
# http://libcloud.readthedocs.org/en/latest/compute/drivers/ec2.html

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

from Cloud import Cloud
from settings import *


class Amazon(Cloud):
    def __init__(self):
        super().__init__()
        amazon = get_driver(Provider.EC2_EU)
        self.driver = amazon(accessKey, secretKey)
        self.publicIP = None

    def create(self):
        print('Retrieving infrastructure information from Amazon ...')

        sizes = self.driver.list_sizes()
        images = self.driver.list_images()

        size = [s for s in sizes if s.id == 't1.micro'][0]
        image = [s for s in images if s.id == 'ami-c7eb65b0'][0]

        print('Done.')
        print('Creating a new kaypair ...')

        self.driver.ex_create_keypair('temp_keypair')

        print('Done.')
        print('Creating a new node ...')

        node = self.driver.create_node(name = 'MongoDB',
                                       size = size,
                                       image = image,
                                       ex_keyname = 'temp_keypair',
                                       ex_security_groups = ['Anywhere'])

        print('Done.')
        print('Waiting for MongoDB ...')

        self.driver.wait_until_running([node])
        self.activeNodes.append(node)

        print('Instance ready.')
        # Doesn't work with EC2: https://github.com/boto/boto/issues/2727
        # print('Attaching a Public IP ...')
        #
        # # noinspection PyPep8Naming
        # self.publicIP = self.driver.ex_allocate_address()
        # self.driver.ex_associate_address_with_node(node, self.publicIP)
        #
        # print('IP address attached.')

    def destroy(self):
        # Doesn't work with EC2: https://github.com/boto/boto/issues/2727
        # print('Releasing public IP ...')
        #
        # self.driver.ex_disassociate_address(self.publicIP)
        # self.publicIP.release()
        #
        # print('Done.')
        print('Destroying the instance on Amazon ...')

        self.activeNode.destroy()

        print('Done.')
        print('Deleting the keypair ...')

        self.driver.ex_delete_keypair('temp_keypair')

        print('Done.')
