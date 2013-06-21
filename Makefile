#
# Generic functions
#

clean_pyc:
	find . -name \*.pyc -delete

#
# Install for development
#

# Install Development Requirements
install_develop:
	./install.sh develop

develop: install_develop

#
# Install for test running
#

# Install Test Requirements
install_test:
	./install.sh test

# Test Command
run_tests:
	python setup.py test

test: install_test run_tests
