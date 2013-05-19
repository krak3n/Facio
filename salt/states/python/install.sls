#
# Install Multiple Python Versions
#
# This state adds a PPA which contains the latest and old python versions
# and installs python 3.2, 3.3, 2.7, 2.6 and the respective -dev counter
# parts.
#

python_install_software_properties:
  pkg:
    - installed
    - name: python-software-properties

python_versions_ppa:
  pkgrepo:
    - managed
    - ppa: fkrull/deadsnakes

{% for v in ["3.3", "3.2", "2.6", "2.7"] %}
python_{{ v|replace(".", "_") }}_install:
  pkg:
    - installed
    - name: python{{ v }}
    - require:
      - pkg: python_install_software_properties
      - pkgrepo: python_versions_ppa

python_{{ v|replace(".", "_") }}_dev_install:
  pkg:
    - installed
    - name: python{{ v }}-dev
    - require:
      - pkg: python_install_software_properties
      - pkg: python_{{ v|replace(".", "_") }}_install
      - pkgrepo: python_versions_ppa
{% endfor %}

# Ensure default Python is installed too w/ pip

{% for pkg in ["python", "python-dev", "python-setuptools"] %}
{{ pkg|replace("-", "_") }}_install:
  pkg:
    - installed
    - name: {{ pkg }}
{% endfor %}

python_install_pip:
  cmd:
    - run
    - name: 'curl -L https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python'
    - unless: 'test -f /usr/local/bin/pip'
    - require:
      - pkg: python_install
      - pkg: python_dev_install
      - pkg: python_setuptools_install
      - pkg: curl_install
