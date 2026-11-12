.PHONY: build check test check-upstream check-annotation check-mixed check-carry
PREFIX ?= .build/install

build:
	sh tools/build.sh

check: test
	python3 -B tools/run.py --prefix "$(PREFIX)"
	python3 -B tools/run_annotation.py --prefix "$(PREFIX)"
	python3 -B tools/run_mixed.py --prefix "$(PREFIX)"
	python3 -B tools/run_carry.py --prefix "$(PREFIX)"

test:
	python3 -B -m unittest discover -s tests -v

check-upstream:
	sh tools/check-upstream.sh

check-annotation:
	python3 -B tools/run_annotation.py --prefix "$(PREFIX)"

check-mixed:
	python3 -B tools/run_mixed.py --prefix "$(PREFIX)"

check-carry:
	python3 -B tools/run_carry.py --prefix "$(PREFIX)"
