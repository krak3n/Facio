#
# Top SLS File
# Kicks things into motion, defining salt modules to run.
#

base:
  '*':
    - misc
    - python
    - facio
    - developer

# vim: set filetype=sls:
