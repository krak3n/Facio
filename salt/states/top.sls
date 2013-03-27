#
# Top SLS File
# Kicks things into motion, defining salt modules to run.
#

base:
  '*':
    - misc
    - python
    - facio

# vim: set filetype=sls:
