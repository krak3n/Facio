#
# Top SLS File
# Kicks things into motion, defining salt modules to run.
#

base:
  '*':
    - packages
    - python
    - facio
    # Local developer states - unique to you - mounted at ~/.salt-dev
    - developer
