.PHONY: install
install:
	pip3 install -r requirements.txt
	echo "Notice: You should install ffmpeg manually for audio apis."

.PHONY: run
run:
	python3 -m src.api

package:
	rm -rf dist/openai.mini
	mkdir dist/openai.mini
	mkdir dist/openai.mini/models
	cp -r .env.example requirements.txt docs Makefile README.md src web dist/openai.mini/
	cd dist && tar zcvf openai.mini.tar.gz openai.mini
