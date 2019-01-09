.PHONY: clean help console virtualenv

help:
        @echo "Usage: make all|env|clean|setup|console"

all: env setup

install:
	@pip install tornado
	@python setup.py install

virtualenv: env
	@(. env/bin/activate; make install)

console: virtualenv
	@(. env/bin/activate; exec poolman_console)

env:
	virtualenv --system-site-packages $@

clean:
	-@rm -rf env dist build *.egg-info
