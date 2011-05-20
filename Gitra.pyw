#!/usr/bin/env python

##    Copyright (C) 2011 Oleg Kertanov <okertanov@gmail.com>
##    All rights reserved.

import sys
from PyQt4 import QtCore, QtGui
import GitLib
from MainWindow import MainWindow

def main():
    app = QtGui.QApplication(sys.argv)

    app.setOrganizationName(GitLib.GITLIBORGNAME)
    app.setOrganizationDomain(GitLib.GITLIBORGDOMAIN)
    app.setApplicationName(GitLib.GITLIBAPPNAME)
    app.setApplicationVersion(GitLib.GITLIBVERSION)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

