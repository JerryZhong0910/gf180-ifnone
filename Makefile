.PHONY: build check test check-upstream
PREFIX ?= .build/install

build:
	sh tools/build.sh

check: test
	python3 -B tools/run.py --prefix "$(PREFIX)"

test:
	python3 -B -m unittest discover -s tests -v

check-upstream:
	sh tools/check-upstream.sh
