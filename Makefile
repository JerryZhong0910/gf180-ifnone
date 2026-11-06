.PHONY: build check
build:
	sh tools/build.sh

check:
	python3 -B tools/run.py
