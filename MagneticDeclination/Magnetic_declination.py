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
__date__ = '2015-05-06'
__copyright__ = '(C) 2015, Aldo Scorza'


from PyQt4.QtCore import *
from PyQt4.QtGui import *
# Initialize Qt resources from file resources.py
import resources

# Import the code for the dialog
from Magnetic_declination_dialog import MagneticDeclinationDialog
import os.path
# IMPORT OTHER
from datetime import *
from . import geomag
from qgis.gui import *
from qgis.core import *
import math
# IMPORT OTHER




class MagneticDeclination(QObject):
    """QGIS Plugin Implementation."""
    #
    def __init__(self, iface):
        QObject.__init__(self)
        """Constructor.
        #
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'MagneticDeclination_{}.qm'.format(locale))
            #
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            #
            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
                #
        # Create the dialog (after translation) and keep reference
        self.dlg = MagneticDeclinationDialog()
        #
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Magnetic Declination')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'MagneticDeclination')
        self.toolbar.setObjectName(u'MagneticDeclination')
        #DECLARATION
        self.dlg.Calculate_Button.clicked.connect(self.simple_Calculate)
        self.dlg.FromMap_Button.clicked.connect(self.simple_FromMap)
        self.dlg.Compass_Button.clicked.connect(self.simple_Compass)
        self.dlg.Cancel_Button.clicked.connect(self.simple_Cancel)
        self.dlg.meter_radioButton.clicked.connect(self.simple_Meter)
        self.dlg.feet_radioButton.clicked.connect(self.simple_Feet)
        self.dlg.toMagnetic_radioButton.clicked.connect(self.simple_ToMag)
        self.dlg.toTrue_radioButton.clicked.connect(self.simple_ToTrue)
        #
        self.dlg.latitude_doubleSpinBox.valueChanged.connect(self.calcSenseLonLat)
        self.dlg.longitude_doubleSpinBox.valueChanged.connect(self.calcSenseLonLat)
        self.dlg.height_doubleSpinBox.valueChanged.connect(self.calcSense)
        self.dlg.heading_doubleSpinBox.valueChanged.connect(self.calcSense)
        self.dlg.d_spinBox.valueChanged.connect(self.calcSense)
        self.dlg.m_spinBox.valueChanged.connect(self.calcSense)
        self.dlg.y_spinBox.valueChanged.connect(self.calcSense)
        self.dlg.height_doubleSpinBox.valueChanged.connect(self.calcSense)
        self.dlg.date_groupBox.clicked.connect(self.calcSense)
        self.dlg.height_groupBox.clicked.connect(self.calcSense)


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.
        #
        We implement this ourselves since we do not inherit QObject.
        #
        :param message: String for translation.
        :type message: str, QString
        #
        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('MagneticDeclination', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.
        #
        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str
        #
        :param text: Text that should be shown in menu items for this action.
        :type text: str
        #
        :param callback: Function to be called when the action is triggered.
        :type callback: function
        #
        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool
        #
        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool
        #
        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool
        #
        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str
        #
        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget
        #
        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.
        #
        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """
        #
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        #
        if status_tip is not None:
            action.setStatusTip(status_tip)
        #
        if whats_this is not None:
            action.setWhatsThis(whats_this)
        #
        if add_to_toolbar:
            self.toolbar.addAction(action)
        #
        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)
        #
        self.actions.append(action)
        #
        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = self.plugin_dir + "/icon.png"
        self.add_action(
            icon_path,
            text=self.tr(u'Magnetic Declination'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Magnetic Declination'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        self.dlg.declination_lineEdit.setText(str(""))
        self.dlg.heading_lineEdit.setText(str(""))
        self.canvasCRS = self.iface.mapCanvas().mapSettings().destinationCrs()
        self.pluginCRS = QgsCoordinateReferenceSystem(4326)
        #
        self.calcSense = 0
        self.SenseFromMap = 0
        #
        self.dlg.show()
        #
        feetmet = self.dlg.meter_radioButton.isChecked()
        magtrue = self.dlg.toMagnetic_radioButton.isChecked()
        #
        if feetmet == 0:
            self.simple_Feet
        else:
            self.simple_Meter
        #
        if magtrue == 0:
            self.simple_ToTrue
        else:
            self.simple_ToMag


        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            pass


    def simple_Meter(self):
    #Define meter
        self.dlg.height_doubleSpinBox.setRange(-10000, 600000)
        self.Runit = "meter"
        return MagneticDeclination.calcSense(self)


    def simple_Feet(self):
    #Define feet
        self.dlg.height_doubleSpinBox.setRange(-3280.840000, 1968503.940000)
        self.Runit = "feet"
        return MagneticDeclination.calcSense(self)


    def simple_ToMag(self):
    #Define magnetic
        self.dlg.heading_label.setText("Magnetic Heading")
        return MagneticDeclination.calcSense(self)


    def simple_ToTrue(self):
    #Define true
        self.dlg.heading_label.setText("True Heading")
        return MagneticDeclination.calcSense(self)


    def calcSense(self):
    #Define sensing
        self.calcSense = 0
        self.dlg.declination_lineEdit.clear()
        self.dlg.heading_lineEdit.clear()


    def calcSenseLonLat(self):
    #Define sensing
        self.calcSense = 0
        self.SenseFromMap = 0
        self.dlg.declination_lineEdit.clear()
        self.dlg.heading_lineEdit.clear()


    def simple_Calculate(self):
    #Define calculate button
        self.simple_latitude = self.dlg.latitude_doubleSpinBox.text()[:-1]
        simple_height = self.dlg.height_doubleSpinBox.text()
        self.simple_longitude = self.dlg.longitude_doubleSpinBox.text()[:-1]
        simple_day = int(self.dlg.d_spinBox.text())
        simple_month = int(self.dlg.m_spinBox.text())
        simple_year = int(self.dlg.y_spinBox.text())
        simple_heading = self.dlg.heading_doubleSpinBox.text()[:-1]
        simple_Xdate = self.dlg.date_groupBox.isChecked()
        simple_Xheight = self.dlg.height_groupBox.isChecked()
        simple_Xmeter = self.dlg.meter_radioButton.isChecked()
        simple_XtoMagnetic = self.dlg.toMagnetic_radioButton.isChecked()
        #
        #DATE CONTROLS
        if simple_Xdate == 0:
            simple_year = date.today().year
            simple_month = date.today().month
            simple_day = date.today().day
        #
        #HEIGHT CONTROLS
        if simple_Xheight == 0:
            simple_Cheight = 0
            self.Runit = "MSL"
            self.Rheight = 0
        else:
            if simple_Xmeter == 0:
                simple_Cheight = float(simple_height)
                self.Runit = "h ft"
                self.Rheight = float(simple_height)
            else:
                simple_Cheight = float(simple_height) * 3.2808399
                self.Runit = "h mt"
                self.Rheight = float(simple_height)
        #
        #TYPE BASED CALCULATION
        self.Rdeclination = geomag.declination(float(self.simple_latitude), float(self.simple_longitude), float(simple_Cheight), date(simple_year,simple_month,simple_day))
        self.Rdate = date(simple_year,simple_month,simple_day)
        if simple_XtoMagnetic == 1:
            Rheading = geomag.mag_heading(float(simple_heading), float(self.simple_latitude), float(self.simple_longitude), float(simple_Cheight), date(simple_year,simple_month,simple_day))
        else:
            Rheading = (float(self.Rdeclination) + float(simple_heading)) % 360
        #
        self.dlg.declination_lineEdit.setText(unicode(str(self.Rdeclination) + u'\u00B0'))
        self.dlg.heading_lineEdit.setText(unicode(str(Rheading) + u'\u00B0'))
        convPoint = QgsCoordinateTransform(self.pluginCRS, self.canvasCRS).transform(QgsPoint(float(self.simple_longitude), float(self.simple_latitude)))
        self.xX = float(convPoint.x())
        self.yY = float(convPoint.y())
        self.calcSense = 1


    def simple_FromMap(self):
    #SELECT COORDS
        self.pointEmitter = QgsMapToolEmitPoint(self.iface.mapCanvas())
        QObject.connect( self.pointEmitter, SIGNAL("canvasClicked(const QgsPoint, Qt::MouseButton)"), self.simple_Point)
        self.iface.mapCanvas().setMapTool( self.pointEmitter )
        self.dlg.hide()
        self.iface.messageBar().pushMessage("", "Waiting for coordinates", level=QgsMessageBar.WARNING,)


    def simple_Point(self, point, button):
    #GET POINT
        self.x = point.x()
        self.y = point.y()
        self.canvasCRS = self.iface.mapCanvas().mapSettings().destinationCrs()
        convPoint = QgsCoordinateTransform(self.canvasCRS, self.pluginCRS).transform(QgsPoint(self.x, self.y))
        self.dlg.longitude_doubleSpinBox.setValue(float(convPoint.x()))
        self.dlg.latitude_doubleSpinBox.setValue(float(convPoint.y()))
        QObject.disconnect( self.pointEmitter, SIGNAL("canvasClicked(const QgsPoint, Qt::MouseButton)"), self.simple_Point)
        self.dlg.show()
        self.iface.messageBar().clearWidgets ()
        self.SenseFromMap = 1


    def simple_Compass(self):
    #INSERT COMPASS
        if self.dlg.declination_lineEdit.text() == "" or self.calcSense == 0:
            QMessageBox.warning( self.iface.mainWindow(),"WARNING", "No value calculated" )
        else:
            if self.SenseFromMap == 1:
                self.pointRose = QgsPoint(self.x, self.y)
            else:
                self.pointRose = QgsPoint(self.xX, self.yY)
            #
            self.iface.mapCanvas().setCenter(self.pointRose)
            self.iface.mapCanvas().refresh ()


            #RUBBER
            self.OriX = self.pointRose.x()
            self.OriY = self.pointRose.y()
            #
            self.rubberCenter = QgsRubberBand(self.iface.mapCanvas(),QGis.Point)
            self.rubberRadius = QgsRubberBand(self.iface.mapCanvas(),QGis.Line )
            self.rubberGhost1 = QgsRubberBand(self.iface.mapCanvas(),QGis.Line )
            self.rubberGhost2 = QgsRubberBand(self.iface.mapCanvas(),QGis.Line )
            self.rubberGhost3 = QgsRubberBand(self.iface.mapCanvas(),QGis.Line )
            self.rubberCenter.setIconSize(10)
            self.rubberRadius.setWidth(5)
            self.rubberGhost1.setWidth(5)
            self.rubberGhost2.setWidth(5)
            self.rubberGhost3.setWidth(5)
            self.rubberCenter.setFillColor(QColor(255,0,0,170))
            self.rubberRadius.setColor(QColor(255,0,0,170))
            self.rubberGhost1.setColor(QColor(255,0,0,170))
            self.rubberGhost2.setColor(QColor(255,0,0,170))
            self.rubberGhost3.setColor(QColor(255,0,0,170))
            self.rubberCenter.addPoint(self.pointRose)
            self.rubberRadius.addPoint(self.pointRose)
            self.rubberGhost1.addPoint(self.pointRose)
            self.rubberGhost2.addPoint(self.pointRose)
            self.rubberGhost3.addPoint(self.pointRose)
            #
            QObject.connect(self.iface.mapCanvas(), SIGNAL("xyCoordinates(const QgsPoint &)"), self.simple_Scale)
            self.dlg.hide()
            self.iface.messageBar().pushMessage("", "Waiting for radius setting", level=QgsMessageBar.WARNING,)


    def simple_Scale(self, point):
    #SET SCALE
        X = point.x()
        Y = point.y()
        self.rubberRadius.movePoint(point)
        #
        rubberGhost1X = ((X-self.OriX)*math.cos(math.radians(90))-(Y-self.OriY)*math.sin(math.radians(90))) + self.OriX
        rubberGhost1Y = ((X-self.OriX)*math.sin(math.radians(90))+(Y-self.OriY)*math.cos(math.radians(90))) + self.OriY
        rubberGhost2X = ((X-self.OriX)*math.cos(math.radians(180))-(Y-self.OriY)*math.sin(math.radians(180))) + self.OriX
        rubberGhost2Y = ((X-self.OriX)*math.sin(math.radians(180))+(Y-self.OriY)*math.cos(math.radians(180))) + self.OriY
        rubberGhost3X = ((X-self.OriX)*math.cos(math.radians(270))-(Y-self.OriY)*math.sin(math.radians(270))) + self.OriX
        rubberGhost3Y = ((X-self.OriX)*math.sin(math.radians(270))+(Y-self.OriY)*math.cos(math.radians(270))) + self.OriY
        #
        self.rubberGhost1.movePoint(QgsPoint(rubberGhost1X, rubberGhost1Y))
        self.rubberGhost2.movePoint(QgsPoint(rubberGhost2X, rubberGhost2Y))
        self.rubberGhost3.movePoint(QgsPoint(rubberGhost3X, rubberGhost3Y))
        #
        self.pointEmitter = QgsMapToolEmitPoint(self.iface.mapCanvas())
        QObject.connect( self.pointEmitter, SIGNAL("canvasClicked(const QgsPoint, Qt::MouseButton)"), self.simple_ComputeScale)
        self.iface.mapCanvas().setMapTool( self.pointEmitter )


    def simple_ComputeScale(self, point, button):
    #COMPUTE SCALE
        self.distance = (QgsGeometry().fromPoint(self.pointRose).distance(QgsGeometry().fromPoint(point)))*2
        self.dlg.show()
        self.iface.messageBar().clearWidgets ()
        #
        self.rubberCenter.reset()
        self.rubberRadius.reset()
        self.rubberGhost1.reset()
        self.rubberGhost2.reset()
        self.rubberGhost3.reset()
        #
        QObject.disconnect(self.iface.mapCanvas(), SIGNAL("xyCoordinates(const QgsPoint &)"), self.simple_Scale)
        QObject.disconnect( self.pointEmitter, SIGNAL("canvasClicked(const QgsPoint, Qt::MouseButton)"), self.simple_ComputeScale)
        return MagneticDeclination.simple_Layer(self)


    def simple_Layer(self):
    #CREATE LAYER
        pointLayer = QgsVectorLayer("Point?crs=" + self.canvasCRS.authid(), "COMPASS ROSE", "memory")
        pointLayer.startEditing()  
        layerData = pointLayer.dataProvider() 
        layerData.addAttributes([
            QgsField("WGS84-lon", QVariant.Double),
            QgsField("WGS84-lat", QVariant.Double),
            QgsField("validity", QVariant.String),
            QgsField("H unit", QVariant.String),
            QgsField("height", QVariant.Double),
            QgsField("declinatio", QVariant.Double),
            QgsField("value", QVariant.String)
            ])
        pointLayer.commitChanges()
        #
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPoint(self.pointRose))
        vaLue = (unicode(("VAR " + str(abs(round(self.Rdeclination, 2))) + u'\u00B0' + "\n" + str(float(round(self.Rheight, 2))) + " " + str(self.Runit) + "\n\n\n\n(" + str(str(self.Rdate)) + ")")))
        #
        feat.setAttributes([
            self.simple_longitude,
            self.simple_latitude,
            str(self.Rdate),
            self.Runit,
            self.Rheight,
            self.Rdeclination,
            vaLue
            ])
        layerData.addFeatures([feat])
        #
        svgStyleTN = {}
        svgStyleTN ['name'] = str(str(self.plugin_dir) + str("/Modern_nautical_compass_rose_TN.svg"))
        svgStyleTN ['size_unit'] = 'MapUnit'
        svgStyleTN ['size'] = str(self.distance)
        svgStyleMN = {}
        svgStyleMN ['name'] = str(str(self.plugin_dir) + str("/Modern_nautical_compass_rose_MN.svg"))
        svgStyleMN ['size_unit'] = 'MapUnit'
        svgStyleMN ['size'] = str(self.distance)
        svgStyleMN ['angle_expression'] = 'declinatio'
        #
        layerTN = QgsSvgMarkerSymbolLayerV2.create(svgStyleTN)
        layerMN = QgsSvgMarkerSymbolLayerV2.create(svgStyleMN)
        pointLayer.rendererV2().symbols()[0].appendSymbolLayer(layerTN)
        pointLayer.rendererV2().symbols()[0].appendSymbolLayer(layerMN)
        #
        palyr = QgsPalLayerSettings()
        palyr.readFromLayer(pointLayer)
        #
        palyr.enabled = True
        palyr.fieldName = "value"
        palyr.placement = int(1)
        palyr.QuadrantPosition = int(4)
        palyr.setDataDefinedProperty(QgsPalLayerSettings.Family, True, True, "'Arial Black'",'')
        palyr.textColor = QColor(229 ,0 ,131)
        palyr.fontSizeInMapUnits = True
        palyr.multilineAlign = int(1)
        palyr.Rotation = float(self.Rdeclination)*-1
        palyr.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, str(self.distance*0.025),'')
        palyr.setDataDefinedProperty(QgsPalLayerSettings.Rotation, True, True, str(float(self.Rdeclination)*-1),'')
        palyr.displayAll = True
        palyr.writeToLayer(pointLayer)
        #
        QgsMapLayerRegistry.instance().addMapLayer(pointLayer)
        self.iface.mapCanvas().refresh()


    def simple_Cancel(self):
    #CLOSE
        self.dlg.close()




