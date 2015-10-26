import getpass
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

# Get the OpenStack drivers
openStack = get_driver(Provider.OPENSTACK)

user = 'benjamin.burgy@master.hes-so.ch'
password = getpass.getpass(prompt='Password: ', stream=None)
tenant = '43303a8189a04df387c58c7499ced0bc'

# Init the driver
driver = openStack(user,
                   password,
                   ex_tenant_name = "benjamin.burgy@master.hes-so.ch",
                   ex_force_auth_url = 'https://keystone.cloud.switch.ch:5000/v2.0/tokens',
                   ex_force_auth_version = '2.0_password',
                   ex_force_service_region = 'ZH')

print driver.list_nodes()
