.PHONY: install
install:
	pip3 install -r requirements.txt
	pip3 install -r app/requirements.txt
	echo "Notice: You should install ffmpeg manually for audio apis."

build:
	cd app/frontend && yarn install && yarn build
.PHONY: run
run-openai:
	python3 -m src.api

run-app:
	python3 -m app.server

