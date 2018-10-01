from os import environ
from os.path import join

#==============================================================================
#                             Package constants
#==============================================================================
PACKAGE_NAME = "poolMan"
PACKAGE_VERSION = 0.01
DEFAULT_CLUSTER_HOSTS = ["localhost"]
DEFAULT_USERNAME = environ["USER"]
DEFAULT_RSA_KEYFILE = join(environ["HOME"], ".ssh", "id_rsa")
DEFAULT_SSH_PORT = 22