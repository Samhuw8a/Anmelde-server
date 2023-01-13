build:
	docker build -t anmelden .

test:
	# python3.10 -m pip install -r requirements.txt
	./links.sh
	mypy --ignore-missing-imports --disallow-untyped-calls src
	python3.10 tests/test.py

run:
	docker run -v $(shell pwd)/logs:/Anmelde_server/logs anmelden
