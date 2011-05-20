
all: gitra
	

gitra: rc.py
	

rc.py:
	pyrcc4 -o MainWindow_rc.py MainWindow.qrc

install:
	

deb:
	

debclean:
	

clean:
	-@rm -f *.pyc MainWindow_rc.py

.PHONY: all gitra install deb debclean clean

.SILENT: clean

