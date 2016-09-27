# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AddPBBMap
                                 A QGIS plugin
 Add PBB Map from postgis database
                              -------------------
        begin                : 2016-09-07
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Septin Mulatsih Rezki
        email                : septinmulatsihrezki@gmail.com
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from qgis.core import QgsVectorLayer, QgsDataSourceURI, QgsMapLayerRegistry
from qgis.core import *
from qgis.utils import *
from PyQt4.QtSql import  *
#import QgsVectorLayer, QgsDataSourceURI
# Initialize Qt resources from file resources.py
# Import the code for the dialog
import os.path
import psycopg2
from PBBMap_dialog import AddPBBMapDialog

class AddPBBMap(QMainWindow, AddPBBMapDialog):
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

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
            'AddPBBMap_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = AddPBBMapDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&AddPBBMap')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'AddPBBMap')
        self.toolbar.setObjectName(u'AddPBBMap')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('AddPBBMap', message)


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

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/AddPBBMap/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Tambah Peta PBB'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&AddPBBMap'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        #Connect to postgre and add to cbo
        conn = psycopg2.connect("dbname='db_pbb' host=localhost port=5433 user='postgres' password='septin'")
        cur = conn.cursor()
        cur.execute("""SELECT wa FROM gis.kecamatan""")
        rows = cur.fetchall()
        row_list = []
        for row in rows:
            #row_list.append(row.)
            self.dlg.cboKecamatan.addItems([row[0]])
        text = str(self.dlg.cboKecamatan.currentText())
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            #Do something useful here - delete the line containing pass and
            # substitute with your code.
            #Versi satu - sudah berhasil, yeay, you know the key right ?
            # show the dialog
            #selectedindexcbo = self.dlg.cboKecamatan.currentIndex()
            #sql = "(SELECT * FROM gis.kec_palu_utm, gis.tm_bidang where gis.kec_palu_utm.wa='TATANGA' AND st_within(gis.tm_bidang.geom, gis.kec_palu_utm.geom) limit 10)"
            #ada ='TATANGA'
            #sql = "(SELECT * from gis.kec_palu_utm where st_area(gis.kec_palu_utm.geom)>200000000)"
            sql = "(SELECT * from gis.kec_palu_utm where wa = '"+text+"')"
            uri = QgsDataSourceURI()
            uri.setConnection("localhost", "5433", "db_pbb", "postgres", "septin")
            uri.setDataSource("", sql, "geom", "", "gid")
            tmadminkec = QgsVectorLayer(uri.uri(), "kec_palu_utm", "postgres")
            QgsMapLayerRegistry.instance().addMapLayer(tmadminkec)
            #tmadminkec.startEditing()
            #iface.actionToggleEditing().setEnabled(True)
            #ada = "TATANGA"
            #sql = "(SELECT * FROM gis.kecamatan where wa=" + ada +")"

            #Versi dua-gagal juga
            #id_field = "gid"
            #table = "(select gid,st_union(geom) from gis.kecamatan group by gid)"
            #uri = "%s key=%s table=%s (geom) sql=" %(db_conn,id_field,table,)
            #layer = QgsVectorLayer(uri,"testlayer", "postgres")
            #QgsMapLayerRegistry.instance().addMapLayer(layer)
            # set database schema, table name, geometry column and optionaly subset(WHERE clause)
            #uri.setDataSource("gis", "tx_bidang", "geom","INSERT INTO gis.tx_bidang(d_nop,d_luas,geom,aktor) select d_nop,d_luas,geom,aktor from gis.tm_bidang where gis.tm_bidang.d_nop = '727102000400302190';")

            # Versi tiga
            #conn = psycopg2.connect("dbname='db_pbb' host=localhost port=5433 user='postgres' password='septin'")
            #cur = conn.cursor()
            #cur.execute("""SELECT wa FROM gis.kecamatan""")
            #db_conn = "dbname='db_pbb' host=localhost port=5433 user='postgres' password='septin'"
            #id_field = "gid"
            #table = "(select * gis.kec_palu_utm)"
            #uri = "%s key=%s table=%s (geom) sql=" % (db_conn, id_field, table,)
            #layer = QgsVectorLayer(uri, "testlayer", "postgres")
            #QgsMapLayerRegistry.instance().addMapLayer(layer)

            #tmlayer.dataProvider()
            #tmlayer.dataProvider().capabilities()
            #tmlayer.startEditing()
            #iface.actionToggleEditing().setEnabled(True)
            #iface.actionToggleEditing().setEnabled(False)

            #uri.setDataSource("gis", "tx_bidang", "geom")
            #txlayer = QgsVectorLayer(uri.uri(), "tx_bidang", "postgres")
            #QgsMapLayerRegistry.instance().addMapLayer(txlayer)




            #uri.setDataSource("gis", "tm_admin_desa", "geom")
            #tmadmindesa = QgsVectorLayer(uri.uri(), "admin desa", "postgres")
            #QgsMapLayerRegistry.instance().addMapLayer(tmadmindesa)
            #tmlayers = tmlayer.exe
            #actions = self.iface.attributesToolbar().action()
            #self.iface.attributesToolbar().addAction()
            #layers = self.iface.legendInterface().layers()
            #layer_list = []
            #for layer in layers:
            #  layer_list.append(layer.name())

            #if layer.name == "tm_layer":
            #   iface.actionToggleEditing().setEnabled(False)
            #else :
            #    iface.actionToggleEditing().setEnabled(True)