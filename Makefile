build:
	docker build -t anmelden .

test:
	# python3.10 -m pip install -r requirements.txt
	./links.sh
	python3.10 tests/test.py
