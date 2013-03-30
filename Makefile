# Install Development Requirements
install_develop_reqs:
	pip install "file://`pwd`#egg=facio[develop]"

# Install Test Requirements
install_test_reqs:
	pip install "file://`pwd`#egg=facio[tests]"

test:
	install_test_reqs
	python setup.py nosetests --include='^(can|it|ensure|must|should|specs?|examples?)' --with-spec --spec-color -s --with-coverage --cover-erase --cover-package=facio
