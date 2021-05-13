
# Makefile for Gravity Server
# Copyright 2019 Creative Collisions Technology, LLC
# Written by: J. Patrick Farrell

INSTALL_DIR=~/bin

all:
	python -m compileall app

build:
	pyinstaller --onefile -p app app/GravityServer.py

install:
	mkdir -p ${INSTALL_DIR}/gravity_app
	cp  app/*.pyc ${INSTALL_DIR}/gravity_app

all:
	pyinstaller --onefile -p app app/GravityServer.py

install:
	mkdir -p ${INSTALL_DIR}
	cp dist/GravityServer ${INSTALL_DIR}
	cp  app/*.pyc ${INSTALL_DIR}/gravity_app

uninstall:
	# Be careful, do not do a blanket remove from the /usr/local/bin directory
	#  because there could be lots of unrelated programs in there that are needed.
	rm -f ${INSTALL_DIR}/GravityServer

clean:
	rm -rf build dist
	rm -f GravityServer.spec
	rm -f MANIFEST
	rm -f app/*.pyc

