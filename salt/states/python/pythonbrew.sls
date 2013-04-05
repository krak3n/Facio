#
# Pythonbrew
# For installing different python versions
#

pythonbrew:
  pip:
    - installed
    - require:
      - pkg: python-pip

pythonbrew_install:
  cmd:
    - run
    - name: pythonbrew_install
    - user: vagrant
    - group: vagrant
    - cwd: /home/vagrant/
    - unless: test -d /home/vagrant/.pythonbrew/
    - require:
      - pip: pythonbrew

pythonbrew_bashrc:
  file:
    - append
    - name: /home/vagrant/.bashrc
    - text: '[[ -s "$HOME/.pythonbrew/etc/bashrc" ]] && source "$HOME/.pythonbrew/etc/bashrc"'
    - require:
      - cmd.run: pythonbrew_install

{# Ubuntu 12.04 Python Version is 2.7 #}
{% for version in '2.6', '3.2' %}
install_py{{ version }}:
  cmd:
    - run
    - name: '/home/vagrant/.pythonbrew/bin/pythonbrew install {{ version }}'
    - user: vagrant
    - group: vagrant
    - cwd: /home/vagrant/
    - unless: test -d /home/vagrant/.pythonbrew/pythons/Python-{{ version }}
    - require:
      - cmd.run: pythonbrew_install

symlimk_py{{ version }}:
  file:
    - symlink
    - name: /usr/bin/python{{ version }}
    - target: /home/vagrant/.pythonbrew/pythons/Python-{{ version }}/bin/python
    - force: True
    - require:
      - cmd.run: install_py{{ version }}
{% endfor %}

# vim: set filetype=sls:
