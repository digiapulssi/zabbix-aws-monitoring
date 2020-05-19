
scripts := $(wildcard ic_aws/*.py)
tests := $(wildcard tests/*.py)

all: clean checkstyle htmlcov dist

checkstyle: $(scripts) $(tests) setup.py
	find . -name "*.py" -exec pycodestyle \{\} --max-line-length=120 \; | tee checkstyle

.coverage: $(scripts) $(tests)	
	coverage run --source ic_aws -m unittest discover -s tests/	

test: .coverage	
	coverage report -m

htmlcov: .coverage	
	coverage html

dist: $(scripts) $(tests) setup.py
	python setup.py sdist --format=gztar

clean:
	rm -rf dist
	rm -rf *.egg-info
	rm -f .coverage
	rm -rf htmlcov
	rm -f checkstyle
	find . -name "*.pyc" -delete
