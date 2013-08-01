#
# Create Facio Virtualenv
#

create_virtualenv_dir:
  file:
    - directory
    - name: /home/vagrant/.virtualenvs
    - make_dirs: True
    - user: vagrant
    - group: vagrant
    - mode: 774

install_virtualenv:
  pip:
    - installed
    - name: virtualenv
    - require:
      - cmd: python_install_pip

install_virtualenv_wrapper:
  pip:
    - installed
    - name: virtualenvwrapper
    - require:
      - pip: install_virtualenv

create_facio_virtualenv:
  virtualenv:
    - managed
    - name: /home/vagrant/.virtualenvs/facio
    - no_site_packages: True
    - runas: vagrant
    - require:
      - file: create_virtualenv_dir
      - pip: install_virtualenv_wrapper
