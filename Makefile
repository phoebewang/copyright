.PHONY: help test

all: help

build:
	python setup.py build --build-base=/tmp/build/copyright

clean:
	-rm -rf dist test/data/tmp
	find . \( -name "*.pyo" -o -name "*.pyc" -o -name "__pycache__" -o -name "tmp*" -o -name "*~" \) -delete
	-rm -f MANIFEST

help:
	@echo make [ clean test sdist build register upload install ]

install:
	python setup.py install

register:
	python setup.py register -r pypi

sdist:
	python setup.py sdist

test:
	for v in 2 3 ; do \
	python$$v -m unittest discover -v ; \
	done

upload:
	python setup.py sdist upload -r pypi
