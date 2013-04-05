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
	nosetests --include='^(can|it|ensure|must|should|specs?|examples?)' --with-spec --spec-color -s --with-coverage --cover-erase --cover-package=facio

test: install_test_reqs run_tests
