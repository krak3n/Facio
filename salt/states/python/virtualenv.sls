#
# Python Virtualenv Setup
# Ensures Virtualenv Wrapper is installed and virtualenvs directory exists
#

virtualenvwrapper:
  pip:
    - installed
    - require:
      - pkg: 'python-pip'

/home/vagrant/.virtualenvs:
  file:
    - directory
    - user: vagrant
    - group: vagrant
    - mode: 755
    - require:
      - pip: virtualenvwrapper

# vim: set filetype=sls:
