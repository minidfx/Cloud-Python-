import getpass

from settings import *

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

# Get the OpenStack drivers
openStack = get_driver(Provider.OPENSTACK)

# Init the driver
driver = openStack(user,
                   password,
                   ex_tenant_name = tenant_name,
                   ex_force_auth_url = auth_url,
                   ex_force_auth_version = '2.0_password',
                   ex_force_service_region = service_region)

print driver.list_nodes()

amazon = get_driver(Provider.EC2_EU_WEST)
driver = amazon(accesskey, secretkey)

print driver.list_nodes()
