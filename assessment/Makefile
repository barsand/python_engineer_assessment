all: run
run:
	./venv/bin/python -m flask --app src.api run

test:
	./venv/bin/python -m unittest discover -s tests/

lint:
	./venv/bin/python -m black src/ tests/

