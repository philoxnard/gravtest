
# Makefile Gravity start/stop script
# Written by: J. Patrick Farrell

USERNAME=pi
BASE_DIR=/home/${USERNAME}

INSTALLDIR=/etc/init.d
SCRIPT_NAME=gravity

all:
	@echo Usage:
	@echo "   make install         (install programs to ${INSTALLDIR})"
	@echo "   make uninstall       (uninstall programs from ${INSTALLDIR})"

install:
	mkdir -p ${BASE_DIR}/scripts
	cp -p ../etc/init.d/${SCRIPT_NAME} ${INSTALLDIR}
	update-rc.d ${SCRIPT_NAME} defaults
	chmod 777 ${INSTALLDIR}/${SCRIPT_NAME}

uninstall:
	rm -f ${INSTALLDIR}/${SCRIPT_NAME}
	rm -rf ${BASE_DIR}/scripts
	update-rc.d ${SCRIPT_NAME} remove

