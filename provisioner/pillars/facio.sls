# Projeect Pillars (Variables)
# These are used by salt states to provision the instance to the pillars below.

# Project
user: vagrant
project_client: 'chris'
project_name: 'facio'

# Paths
root_dir: /home/vagrant
virtualenv_dir: /home/vagrant/.virtualenvs
home_dir: /home/vagrant

# Config
post_activate: /home/vagrant/.virtualenvs/facio/bin/postactivate

# vim: set filetype=sls:
