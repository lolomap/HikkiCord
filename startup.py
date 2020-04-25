from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QSystemTrayIcon, \
    QMenu, QAction, QStyle, qApp, QComboBox, QSlider, QPushButton, QMessageBox
from PyQt5.QtCore import QSize, Qt
import os
import subprocess


class MainWindow(QMainWindow):
    """
         Сheckbox and system tray icons.
         Will initialize in the constructor.
    """
    tray_icon = None

    def quit_util(self):
        subprocess.check_call("TASKKILL /F /PID {pid} /T".format(pid=self.script.pid))
        qApp.quit()

    # Override the class constructor
    def __init__(self):
        # Be sure to call the super class method
        QMainWindow.__init__(self)

        self.script = None

        self.setMinimumSize(QSize(350, 150))  # Set sizes
        self.setMaximumSize(QSize(350, 150))
        self.setWindowTitle("HikkiCord")  # Set a title
        self.setWindowIcon(QIcon('discord.ico'))
        central_widget = QWidget(self)  # Create a central widget
        self.setCentralWidget(central_widget)  # Set the central widget

        grid_layout = QGridLayout(self)  # Create a QGridLayout
        central_widget.setLayout(grid_layout)  # Set the layout into the central widget
        # grid_layout.addWidget(QLabel("Application started successful", self), 0, 0)
        grid_layout.addWidget(QLabel("Выберите свой браузер: ", self), 1, 0)

        self.browser_box = QComboBox(self)
        self.browser_box.addItems(['Chrome', 'Opera'])
        grid_layout.addWidget(self.browser_box, 1, 1)

        grid_layout.addWidget(QLabel("Частота обновления: раз в ", self), 2, 0)

        self.delay_slider = QSlider(Qt.Horizontal, self)
        self.delay_slider.setValue(60)
        self.delay_slider.valueChanged[int].connect(self.change_value)

        grid_layout.addWidget(self.delay_slider, 2, 1)

        self.delay_preview = QLabel("60", self)
        grid_layout.addWidget(self.delay_preview, 2, 2)
        grid_layout.addWidget(QLabel('секунд'), 2, 3)

        self.save_button = QPushButton('Сохранить')
        self.save_button.clicked.connect(self.safe_settings)
        grid_layout.addWidget(self.save_button, 3, 0)

        self.stop_button = QPushButton('Остановить')
        self.stop_button.setCheckable(True)
        self.stop_button.clicked[bool].connect(self.stop)
        grid_layout.addWidget(self.stop_button, 3, 1)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('discord.ico'))
        # self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        '''
            Define and add steps to work with the system tray icon
            show - show window
            hide - hide window
            exit - exit from application
        '''
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.quit_util)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def stop(self, state):
        if state:
            subprocess.check_call("TASKKILL /F /PID {pid} /T".format(pid=self.script.pid))
        else:
            mw.script = subprocess.Popen('../hc_main.exe')

    def change_value(self, value):
        self.delay_preview.setText(str(value))

    def safe_settings(self):
        try:
            f = open('settings.txt', 'w')
            f.write('browser:'+self.browser_box.currentText()+'\ndelay:'+str(int(self.delay_slider.value())))
            f.close()
        except Exception as e:
            QMessageBox.warning(self, 'Save error', 'Error: '+str(e))

    # Override closeEvent, to intercept the window closing event
    # The window will be closed only if there is no check mark in the check box
    def closeEvent(self, event):
        event.ignore()
        self.hide()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()

    # os.system('hc_main.exe')
    mw.script = subprocess.Popen('../hc_main.exe')

    mw.show()
    sys.exit(app.exec())
