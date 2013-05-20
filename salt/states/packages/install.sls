#
# Common package installation
#

{% for pkg in 'build-essential', 'htop', 'nmap', 'curl', 'tree', 'git-core', 'git', 'wget', 'unzip', 'ncdu', 'tzdata', 'alpine', 'git-flow' %}
{{ pkg|replace("-", "_") }}_install:
  pkg:
    - installed
    - name: {{ pkg }}
{% endfor %}
