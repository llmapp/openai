.PHONY: install
install:
	pip3 install -r requirements.txt

.PHONY: run
run:
	python3 -m src.api
