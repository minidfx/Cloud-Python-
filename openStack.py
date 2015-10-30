from libcloud.compute.types import Provider, NodeState
from libcloud.compute.providers import get_driver
import time

from settings import *


class OpenStack:
    def __init__(self):
        # Get the OpenStack drivers
        openstack = get_driver(Provider.OPENSTACK)

        # Init the driver
        self.driver = openstack(user,
                                password,
                                ex_tenant_name=tenant_name,
                                ex_force_auth_url=auth_url,
                                ex_force_auth_version='2.0_password',
                                ex_force_service_region=service_region)

    def create(self):
        print('Reading available infrastructure from Swith-Engine ...')

        sizes = self.driver.list_sizes()
        images = self.driver.list_images()
        security_groups = self.driver.ex_list_security_groups()
        networks = self.driver.ex_list_networks()
        ips = self.driver.ex_list_floating_ips()

        size = [s for s in sizes if s.name == 'c1.micro'][0]
        image = [s for s in images if s.id == '93231f46-2e7c-4d3a-838d-460492e6e266'][0]
        security_group = [s for s in security_groups if s.name == 'anywhere'][0]
        network = [s for s in networks if s.name == 'My network'][0]
        ip = [s for s in ips if s.id == '5e378f57-2499-49c0-984a-1bb80102894b'][0]

        print("Creating a new node ...")

        # Create a micro node
        self.driver.create_node(name='MongoDB',
                                size=size,
                                image=image,
                                ex_security_groups=[security_group],
                                ex_keyname='switch-engine',
                                networks=[network])

        print("Created")

        nodes = self.driver.list_nodes()
        node = [s for s in nodes if s.name == 'MongoDB'][0]

        while node.state != NodeState.RUNNING:
            print('Waiting for MongoDB ...')
            time.sleep(1)

            nodes = self.driver.list_nodes()
            node = [s for s in nodes if s.name == 'MongoDB'][0]

        self.activeNode = node
        print('Instance ready.')
        print('Attaching an IP address ...')

        self.driver.ex_attach_floating_ip_to_node(node, ip)

        print("IP address attached.")

    def destroy(self):
        print("Destroying the previous one created ...")

        self.activeNode.destroy()

        print("Destroyed")
