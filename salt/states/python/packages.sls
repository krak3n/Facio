#
# Packages required for Python
#

{% for package in 'python', 'python-dev', 'python-virtualenv', 'python-pip'  %}
{{ package }}:
  pkg:
    - installed
{% endfor %}

# vim: set filetype=sls:
