#
# Generic Methods
#

install_facio:
	pip install -q -e . --use-mirrors

#
# Development methods
#

# Install Development Requirements
install_develop_reqs:
	pip install -q "file://`pwd`#egg=facio[develop]"

develop: install_develop_reqs install_facio

#
# Testing methods
#

# Install Test Requirements
install_test_reqs:
	pip install -q "file://`pwd`#egg=facio[tests]"

# Test Command
run_tests:
	python setup.py test

test: install_test_reqs run_tests
