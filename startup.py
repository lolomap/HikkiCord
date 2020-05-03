from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QSystemTrayIcon, \
    QMenu, QAction, QStyle, qApp, QComboBox, QSlider, QPushButton, QMessageBox, QCheckBox, QLineEdit
from PyQt5.QtCore import QSize, Qt
import subprocess

SCRIPT_PATH = 'bin/hc_main.exe'


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

        self.setMinimumSize(QSize(370, 250))  # Set sizes
        self.setMaximumSize(QSize(370, 250))
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
        self.delay_slider.setValue(0)
        self.delay_slider.valueChanged[int].connect(self.change_value)

        grid_layout.addWidget(self.delay_slider, 2, 1)

        self.delay_preview = QLabel("0 секунд", self)
        grid_layout.addWidget(self.delay_preview, 2, 2)

        grid_layout.addWidget(QLabel('Отображать:'), 3, 0)
        self.is_yt_checkbox = QCheckBox('Youtube видео')
        grid_layout.addWidget(self.is_yt_checkbox, 4, 0)
        self.is_anime = QCheckBox('Аниме')
        grid_layout.addWidget(self.is_anime, 5, 0)
        self.is_ide = QCheckBox('Работу в IDE')
        grid_layout.addWidget(self.is_ide, 6, 0)
        self.is_vk_online = QCheckBox('Онлайн в VK')
        self.is_vk_online.stateChanged[int].connect(self.disable_id_field)
        grid_layout.addWidget(self.is_vk_online, 7, 0)

        self.id_field = QLineEdit()
        grid_layout.addWidget(QLabel('ID страницы:'), 8, 0)
        if not self.is_vk_online.isChecked():
            self.id_field.setEnabled(False)
        grid_layout.addWidget(self.id_field, 8, 1)

        self.save_button = QPushButton('Сохранить')
        self.save_button.clicked.connect(self.safe_settings)
        grid_layout.addWidget(self.save_button, 9, 0)

        self.stop_button = QPushButton('Остановить')
        self.stop_button.setCheckable(True)
        self.stop_button.clicked[bool].connect(self.stop)
        grid_layout.addWidget(self.stop_button, 9, 1)

        self.restart_button = QPushButton('Перезапустить')
        self.restart_button.clicked.connect(self.restart)
        grid_layout.addWidget(self.restart_button, 9, 2)

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

    def disable_id_field(self, state):
        if state:
            self.id_field.setEnabled(True)
        else:
            self.id_field.setEnabled(False)

    def stop(self, state):
        if state:
            subprocess.check_call("TASKKILL /F /PID {pid} /T".format(pid=self.script.pid))
        else:
            mw.script = subprocess.Popen(SCRIPT_PATH)

    def restart(self):
        subprocess.check_call("TASKKILL /F /PID {pid} /T".format(pid=self.script.pid))
        mw.script = subprocess.Popen(SCRIPT_PATH)

    def change_value(self, value):
        self.delay_preview.setText(str(value) + ' секунд')

    def safe_settings(self):
        try:
            f = open('settings.txt', 'w')
            settings = 'browser:'+self.browser_box.currentText()+'\n'
            settings = settings + 'delay:'+str(int(self.delay_slider.value()))+'\n'
            settings = settings + 'yt:'+str(self.is_yt_checkbox.isChecked())+'\n'
            settings = settings + 'anime:' + str(self.is_anime.isChecked()) + '\n'
            settings = settings + 'ide:' + str(self.is_ide.isChecked()) + '\n'
            settings = settings + 'vk_online:' + str(self.is_vk_online.isChecked()) + '\n'
            settings = settings + 'vk_id:' + self.id_field.text()
            f.write(settings)
            f.close()
            if self.id_field.text() == 'id263351923':
                QMessageBox.warning(self, 'Warning', 'Пидорас поставь нормальный id')
        except Exception as e:
            QMessageBox.warning(self, 'Save error', 'Error: '+str(e))

    def load_settings(self):
        try:
            settings = open('settings.txt').read().split('\n')
            client_str = settings[0].split(':')[1]
            delay = int(settings[1].split(':')[1]) * 1000
            if settings[2].split(':')[1] == 'True':
                is_yt = True
            else:
                is_yt = False
            if settings[3].split(':')[1] == 'True':
                is_anime = True
            else:
                is_anime = False
            if settings[4].split(':')[1] == 'True':
                is_ide = True
            else:
                is_ide = False
            if settings[5].split(':')[1] == 'True':
                is_vk_online = True
            else:
                is_vk_online = False

            user_id = settings[6].split(':')[1]

            self.browser_box.setCurrentText(client_str)
            self.delay_slider.setValue(delay)
            self.is_yt_checkbox.setChecked(is_yt)
            self.is_anime.setChecked(is_anime)
            self.is_ide.setChecked(is_ide)
            self.is_vk_online.setChecked(is_vk_online)
            self.id_field.setText(user_id)

        except IndexError:
            return

    # Override closeEvent, to intercept the window closing event
    # The window will be closed only if there is no check mark in the check box
    def closeEvent(self, event):
        event.ignore()
        self.hide()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.load_settings()

    # mw.script = subprocess.Popen(SCRIPT_PATH)

    mw.show()
    sys.exit(app.exec())
