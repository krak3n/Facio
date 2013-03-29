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

watchdog:
  pip:
    - installed
    - user: vagrant
    - bin_env: /home/vagrant/.virtualenvs/facio/bin/pip
    - require:
      - virtualenv: facio_virtualenv

install_reqs:
  cmd:
    - run
    - name: /home/vagrant/.virtualenvs/facio/bin/pip install -r /home/vagrant/facio/facio/requirements.txt
    - user: vagrant
    - group: vagrant
    - require:
      - virtualenv: facio_virtualenv

# vim: set filetype=sls:
