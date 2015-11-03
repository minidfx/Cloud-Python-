# Getting started with OpenStack using libcloud
# http://developer.openstack.org/firstapp-libcloud/getting_started.html
from libcloud.compute.ssh import *
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from Cloud import Cloud
from settings import *


# noinspection PyPep8Naming
class OpenStack(Cloud):
    def __init__(self):
        super().__init__()
        openstack = get_driver(Provider.OPENSTACK)
        self.driver = openstack(user,
                                password,
                                ex_tenant_name = tenant_name,
                                ex_force_auth_url = auth_url,
                                ex_force_auth_version = '2.0_password',
                                ex_force_service_region = service_region)
        self.activeIps = []

    def create(self):
        print('Retrieving infrastructure information from SwitchEngines ...')

        images = self.driver.list_images()
        sizes = self.driver.list_sizes()
        security_groups = self.driver.ex_list_security_groups()
        networks = self.driver.ex_list_networks()

        print('Done.')

        security_group = [s for s in security_groups if s.name == 'anywhere'][0]
        network = [s for s in networks if s.name == 'My network'][0]

        size = [s for s in sizes if s.name == 'c1.micro'][0]

        # noinspection PyPep8Naming
        mongoDbIp = self.__run_instance('MongoDB', size, images, security_group, network)
        restServerIP = self.__run_instance('RESTServer', size, images, security_group, network)
        restClientIP = self.__run_instance('RESTClient', size, images, security_group, network)

        self.__additionalOperations(restServerIP, restClientIP, mongoDbIp)

    @staticmethod
    def __additionalOperations(restServerIP, restClientIP, mongoDbIp):
        clientSSH = ShellOutSSHClient(restServerIP, username = 'ubuntu')
        clientSSH.connect()

        try:
            clientSSH.run('python /home/ubuntu/Downloads/pyserver.py %s &' % mongoDbIp)
        finally:
            clientSSH.close()

        clientSSH = ShellOutSSHClient(restClientIP, username = 'ubuntu')
        clientSSH.connect()

        try:
            clientSSH.run('python /home/ubuntu/Downloads/pyclient.py %s &' % mongoDbIp)
        finally:
            clientSSH.close()

    def __run_instance(self, instancename, size, images, security_group, network):
        print('Creating a new node ...')

        image = [s for s in images if s.name == instancename][0]

        node = self.driver.create_node(name = instancename,
                                       size = size,
                                       image = image,
                                       ex_security_groups = [security_group],
                                       ex_keyname = 'switch-engine',
                                       networks = [network])

        print('Done.')
        print("Waiting for %s ..." % instancename)

        self.driver.wait_until_running([node])
        self.activeNodes.append(node)

        nodes = self.driver.list_nodes()
        instanceNode = [s for s in nodes if s.name == instancename][0]
        privateIp = instanceNode.private_ips[0]

        print('Instance ready.')
        print('Attaching a Public IP ...')

        ip = self.driver.ex_create_floating_ip()
        self.activeIps.append(ip)
        self.driver.ex_attach_floating_ip_to_node(node, ip)

        print('Done.')

        return privateIp

    def destroy(self):
        print('Destroying the instance on SwitchEngines ...')

        for node in self.activeNodes:
            node.destroy()

        for ip in self.activeIps:
            self.driver.ex_delete_floating_ip(ip)

        print('Done.')
