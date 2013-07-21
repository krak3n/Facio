#
# Top SLS File
# Kicks things into motion, defining salt modules to run.
#

base:
  '*':
    - packages
    - python
    - facio
    # Local states - unique to you - mounted at ~/.salt
    - local
