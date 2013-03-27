#
# Facio States
# States specific to Facio Development
#

facio_virtualenv:
  virtualenv:
    - managed
    - name: /home/vagrant/.virtualenvs/facio
    - no_site_packages: True
    - runas: vagrant
    - require:
      - file.directory: /home/vagrant/.virtualenvs
      - pkg: python-virtualenv

# vim: set filetype=sls:
