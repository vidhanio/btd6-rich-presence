import time, argparse, json, configparser, pprint, sys
from rapidfuzz import fuzz, process
from pypresence import Presence
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QGridLayout,
    QWidget,
    QCheckBox,
    QSystemTrayIcon,
    QSpacerItem,
    QSizePolicy,
    QMenu,
    QAction,
    QStyle,
    qApp,
    QComboBox,
    QSpinBox,
    QPushButton,
    QMenuBar,
    QStatusBar,
)
from PyQt5 import QtCore, QtGui

config = configparser.ConfigParser()
config.read("config.ini")

assets = json.load(open("assets.json", "r"))

client_id = config["Rich Presence"]["client_id"]
RPC = Presence(client_id)
RPC.connect()
RPC.update(large_image="icon", large_text="Bloons TD 6", details="In Menu")
start_time = time.time()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setObjectName("MainWindow")
        self.resize(700, 500)

        self.map_lb = QLabel(self)
        self.map_lb.setGeometry(QtCore.QRect(25, 25, 200, 25))
        self.map_lb.setObjectName("map_lb")

        self.map_cb = QComboBox(self)
        self.map_cb.setGeometry(QtCore.QRect(25, 50, 200, 25))
        self.map_cb.setObjectName("map_cb")
        self.map_cb.addItems(assets["maps"].keys())

        self.difficulty_lb = QLabel(self)
        self.difficulty_lb.setGeometry(QtCore.QRect(25, 100, 200, 25))
        self.difficulty_lb.setObjectName("difficulty_lb")

        self.difficulty_cb = QComboBox(self)
        self.difficulty_cb.setGeometry(QtCore.QRect(25, 125, 200, 25))
        self.difficulty_cb.addItems(assets["difficulties"].keys())
        self.difficulty_cb.setObjectName("difficulty_cb")

        self.variation_lb = QLabel(self)
        self.variation_lb.setGeometry(QtCore.QRect(25, 175, 200, 25))
        self.variation_lb.setObjectName("variation_lb")

        self.variation_cb = QComboBox(self)
        self.variation_cb.setGeometry(QtCore.QRect(25, 200, 200, 25))
        self.variation_cb.setObjectName("variation_cb")
        self.variations_gen()
        self.difficulty_cb.currentTextChanged.connect(self.variations_gen)

        self.coop_lb = QLabel(self)
        self.coop_lb.setGeometry(QtCore.QRect(25, 250, 200, 25))
        self.coop_lb.setObjectName("coop_lb")

        self.coop_sb = QSpinBox(self)
        self.coop_sb.setGeometry(QtCore.QRect(25, 275, 50, 25))
        self.coop_sb.setObjectName("coop_sb")
        self.coop_sb.setRange(1, 4)

        self.update_bt = QPushButton(self)
        self.update_bt.setGeometry(QtCore.QRect(25, 325, 200, 100))
        self.update_bt.setObjectName("update_bt.")
        self.update_bt.clicked.connect(self.update_presence)

        self.map_image = QLabel(self)
        self.map_image.setGeometry(QtCore.QRect(250, 25, 412, 266))
        self.map_image.setText("")
        self.map_image.setScaledContents(True)
        self.map_image.setObjectName("map_image")
        self.map_image_set()
        self.map_cb.currentTextChanged.connect(self.map_image_set)

        self.variation_image = QLabel(self)
        self.variation_image.setGeometry(QtCore.QRect(250, 191, 100, 100))
        self.variation_image.setText("")
        self.variation_image.setScaledContents(True)
        self.variation_image.setObjectName("variation_image")
        self.variation_image_set()
        self.difficulty_cb.currentTextChanged.connect(self.variation_image_set)
        self.variation_cb.currentTextChanged.connect(self.variation_image_set)

        self.coop_image = QLabel(self)
        self.coop_image.setGeometry(QtCore.QRect(350, 191, 100, 100))
        self.coop_image.setText("")
        self.coop_image.setScaledContents(True)
        self.coop_image.setObjectName("coop_image")
        self.players_image_set()
        self.coop_sb.valueChanged.connect(self.players_image_set)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon("assets/icon.png"))
        self.show_action = QAction("Show", self)
        self.quit_action = QAction("Exit", self)
        self.hide_action = QAction("Hide", self)
        self.show_action.triggered.connect(self.show)
        self.hide_action.triggered.connect(self.hide)
        self.quit_action.triggered.connect(qApp.quit)
        self.tray_menu = QMenu()
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addAction(self.hide_action)
        self.tray_menu.addAction(self.quit_action)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.hide_and_show)

        self.tray_icon.show()

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.retranslateUi(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Bloons TD 6 Rich Presence"))
        self.map_lb.setText(_translate("MainWindow", "Map"))
        self.difficulty_lb.setText(_translate("MainWindow", "Difficulty"))
        self.variation_lb.setText(_translate("MainWindow", "Variation"))
        self.coop_lb.setText(_translate("MainWindow", "Player Count"))
        self.update_bt.setText(_translate("MainWindow", "Update"))

    def map_image_set(self):
        self.map_image.setPixmap(
            QtGui.QPixmap(
                "assets/original/maps/"
                + assets["maps"][self.map_cb.currentText()]["image"]
                + ".png"
            )
        )

    def variation_image_set(self):
        if self.variation_cb.currentText() != "":
            self.variation_image.setPixmap(
                QtGui.QPixmap(
                    "assets/difficulties/"
                    + assets["difficulties"][self.difficulty_cb.currentText()][
                        "variations"
                    ][self.variation_cb.currentText()]["image"]
                    + ".png"
                )
            )

    def players_image_set(self):
        self.coop_image.setPixmap(
            QtGui.QPixmap("assets/coop/" + str(self.coop_sb.value()) + ".png")
        )

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def hide_and_show(self, reason):
        if reason == 3:
            if self.isHidden():
                self.show()
            else:
                self.hide()
        elif reason == 2:
            if self.isHidden():
                self.hide()
            else:
                self.show()

    def variations_gen(self):
        self.variation_cb.clear()
        self.variation_cb.addItems(
            assets["difficulties"][self.difficulty_cb.currentText()][
                "variations"
            ].keys()
        )
        self.variation_cb.setCurrentIndex(
            list(
                assets["difficulties"][self.difficulty_cb.currentText()][
                    "variations"
                ].keys()
            ).index("standard")
        )

    def return_values(self):
        a = {
            "map_image": assets["maps"][self.map_cb.currentText()]["image"],
            "map_hf": assets["maps"][self.map_cb.currentText()]["name_hf"],
            "difficulty_hf": assets["difficulties"][self.difficulty_cb.currentText()][
                "name_hf"
            ],
            "variation_image": assets["difficulties"][self.difficulty_cb.currentText()][
                "variations"
            ][self.variation_cb.currentText()]["image"],
            "variation_hf": assets["difficulties"][self.difficulty_cb.currentText()][
                "variations"
            ][self.variation_cb.currentText()]["name_hf"],
            "icon": "icon",
        }
        return a

    def presence_gen(self):
        pg_formatdict = self.return_values()
        pg_presencedict = {}
        for pg_field in list(config["Map, Difficulty"].keys()):
            pg_presencedict[pg_field] = config["Map, Difficulty"][pg_field].format(
                **pg_formatdict
            )
        pg_presencedict["party_size"] = []
        pg_presencedict["start"] = time.time()
        if self.coop_sb.value() != 1:
            for pg_field in list(config["Co-Op"].keys()):
                pg_presencedict[pg_field] = config["Co-Op"][pg_field].format(
                    **pg_formatdict
                )
                pg_presencedict["party_size"] = [self.coop_sb.value(), 4]
        for pg_field in list(pg_presencedict.keys()):
            if pg_presencedict[pg_field] == "" or pg_presencedict[pg_field] == []:
                pg_presencedict[pg_field] = None
        return pg_presencedict

    def update_presence(self):
        pvars = self.presence_gen()
        RPC.update(
            large_image=pvars["large_image"],
            large_text=pvars["large_text"],
            small_image=pvars["small_image"],
            small_text=pvars["small_text"],
            details=pvars["details"],
            state=pvars["state"],
            party_size=pvars["party_size"],
            start=pvars["start"],
        )


app = QApplication(sys.argv)
mw = MainWindow()
mw.show()
sys.exit(app.exec())
