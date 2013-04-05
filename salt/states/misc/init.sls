#
# Misc States, i.e Common packages like tree, top and what not, stuff that requires no further config other than
# to be installed.
#

{% for package in 'build-essential', 'python-software-properties', 'htop', 'nmap', 'curl', 'tree', 'git-core', 'git', 'wget', 'unzip', 'ncdu', 'tzdata', 'alpine', 'git-flow' %}
{{ package }}:
  pkg:
    - installed
{% endfor %}

# vim: set filetype=sls:
