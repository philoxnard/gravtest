# Makefile for Gravity Documentation
# --pfarrell

INSTALL_DIR=../public

all:
	mkdir -p html
	pandoc gravity_initial_setup.md -o html/gravity_initial_setup.html --css=css/main.css
	cp -a html/* ../public

install:
	mkdir -p ${INSTALL_DIR}
	cp -a html/* ${INSTALL_DIR}

clean:
	rm -rf html
	rm -rf pdf