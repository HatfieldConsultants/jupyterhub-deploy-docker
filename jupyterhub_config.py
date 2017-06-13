# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

c = get_config()

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
# Spawn containers from this image
c.DockerSpawner.container_image = os.environ['DOCKER_NOTEBOOK_IMAGE']
# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd })
# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }
# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }
c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'local' })
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8080
c.NotebookApp.allow_origin = '*'

# TLS config
c.JupyterHub.port = 80

c.JupyterHub.authenticator_class = 'ldapauthenticator.ldapauthenticator.LDAPLocalAuthenticator'                                                                                                                    
c.LDAPAuthenticator.server_address = '192.168.10.8'                                                                                                                                                                
c.LDAPAuthenticator.server_port = 3268                                                                                                                                                                             
c.LDAPAuthenticator.use_ssl = False                                                                                                                                                                                
c.LDAPAuthenticator.bind_dn_template = '{username}'                                                                                                                                                                
c.LDAPAuthenticator.lookup_dn = True                                                                                                                                                                               
c.LDAPAuthenticator.lookup_dn_search_user = 'CN=Some Guy,ou=NV_Users,ou=Vancouver,ou=HatfieldGroup,dc=HATCON,dc=local'                                                                                          
c.LDAPAuthenticator.lookup_dn_search_password = 'ThisIsntARealPassword'
c.LDAPAuthenticator.user_search_base = 'OU=HatfieldGroup,DC=HATCON,DC=local'                                                                                                                                       
c.LDAPAuthenticator.user_attribute = 'sAMAccountName'                                                                                                                                                              
c.LDAPAuthenticator.create_system_users = True                                                                                                                                                                     
c.Authenticator.add_user_cmd =  ['sudo', 'adduser', '-q', '--gecos', '""', '--disabled-password']                                                                                                                  
c.LDAPAuthenticator.lookup_dn_user_dn_attribute = 'cn'

# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')
c.JupyterHub.db_url = os.path.join('sqlite:///', data_dir, 'jupyterhub.sqlite')
c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
    'jupyterhub_cookie_secret')

# Whitlelist users and admins
c.Authenticator.admin_users = {'asoltys', 'jsuwala', 'zlu'}
c.JupyterHub.admin_access = True
