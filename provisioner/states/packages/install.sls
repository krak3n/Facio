#
# Common package installation
#

{% for pkg in 'build-essential', 'htop', 'nmap', 'curl', 'tree', 'git', 'mercurial', 'wget', 'unzip', 'ncdu', 'tzdata', 'alpine', 'git-flow' %}
{{ pkg|replace("-", "_") }}_install:
  pkg:
    - installed
    - name: {{ pkg }}
{% endfor %}
