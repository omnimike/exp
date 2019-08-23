.PHONY: all dev watch static-test-files clean

all: dev

dev: static-test-files
	$(shell npm bin)/webpack --config webpack.config.js

watch: static-test-files
	$(shell npm bin)/webpack-dev-server --config webpack.config.js --content-base build

clean:
	rm -rf build
	mkdir -p build

static-test-files: build/index.html build/increment.html build/layouts.html

build/%.html: test/pages/%.html build-dir
	cp $< $@

build-dir:
	mkdir -p build
