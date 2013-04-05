#
# Development methods
#

# Install Development Requirements
install_develop_reqs:
	pip install -q "file://`pwd`#egg=facio[develop]"

develop: install_develop_reqs

#
# Testing methods
#

# Install Test Requirements
install_test_reqs:
	pip install -q "file://`pwd`#egg=facio[tests]"

test: install_test_reqs
