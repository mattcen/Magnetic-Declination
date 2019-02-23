# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MagneticDeclination
                              -------------------
        begin                : 2015-04-08
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Aldo Scorza
        email                : hacked dot crew at gmail dot com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
__author__ = 'Aldo Scorza'
__date__ = '2019-02-14'
__copyright__ = '(C) 2015, Aldo Scorza'


import os

from qgis.PyQt import QtGui, uic, QtCore, QtWidgets

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Magnetic_declination_dialog_base.ui'))


class MagneticDeclinationDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(MagneticDeclinationDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

