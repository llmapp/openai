.PHONY: install
install:
	pip3 install -r requirements.txt
	echo "Notice: You should install ffmpeg manually for audio apis."

.PHONY: run
run:
	python3 -m src.api
