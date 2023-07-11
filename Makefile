.PHONY: dev
dev:
	pip3 install -r requirements.txt
	python3 -m uvicorn src.api:api --reload
