# Getting started with OpenStack using libcloud
# http://developer.openstack.org/firstapp-libcloud/getting_started.html

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

from Cloud import Cloud
from settings import *


class OpenStack(Cloud):
    def __init__(self):
        super(self).__init__()
        openstack = get_driver(Provider.OPENSTACK)
        self.driver = openstack(user,
                                password,
                                ex_tenant_name = tenant,
                                ex_force_auth_url = auth_url,
                                ex_force_auth_version = '2.0_password',
                                ex_force_service_region = service_region)

    def create(self):
        print('Retrieving infrastructure information from SwitchEngines ...')

        sizes = self.driver.list_sizes()
        images = self.driver.list_images()
        security_groups = self.driver.ex_list_security_groups()
        networks = self.driver.ex_list_networks()
        ips = self.driver.ex_list_floating_ips()

        print('Done.')

        size = [s for s in sizes if s.name == 'c1.micro'][0]
        image = [s for s in images if s.id == '93231f46-2e7c-4d3a-838d-460492e6e266'][0]
        security_group = [s for s in security_groups if s.name == 'anywhere'][0]
        network = [s for s in networks if s.name == 'My network'][0]
        ip = [s for s in ips if s.id == '5e378f57-2499-49c0-984a-1bb80102894b'][0]

        self.__run_instance('MongoDB', size, image, security_group, network)
        self.__run_instance('RESTServer', size, image, security_group, network)
        self.__run_instance('RESTClient', size, image, security_group, network)

    def __run_instance(self, instancename, size, image, security_group, network):
        print('Creating a new node ...')

        # Create a micro node
        node = self.driver.create_node(name = instancename,
                                       size = size,
                                       image = image,
                                       ex_security_groups = [security_group],
                                       ex_keyname = 'switch-engine',
                                       networks = [network])

        print('Done.')
        print('Waiting for MongoDB ...')

        self.driver.wait_until_running([node])
        self.activeNode = node

        print('Instance ready.')
        print('Attaching a Public IP ...')

        self.driver.ex_attach_floating_ip_to_node(node, ip)

        print('Done.')

    def destroy(self):
        print('Destroying the instance on SwitchEngines ...')

        self.activeNode.destroy()

        print('Done.')
