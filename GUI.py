from Gui.ui_Timer_ui import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow, QSystemTrayIcon, QStyle, QMenu
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QAction

from os import system

from Time_format import add_zero, s_in_m_h, h_m_in_s

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_clear.clicked.connect(self.cancel_timer)
        self.ui.pushButton_FAQ_add.clicked.connect(self.msg_FAQ_action)
        self.ui.pushButton_FAQ.clicked.connect(self.msg_FAQ)
        self.ui.pushButton_add_1.clicked.connect(self.click_btn_add_1)
        self.ui.pushButton_add_5.clicked.connect(self.click_btn_add_5)
        self.ui.pushButton_add_10.clicked.connect(self.click_btn_add_10)
        self.ui.pushButton_add_20.clicked.connect(self.click_btn_add_20)
        self.ui.pushButton_add_30.clicked.connect(self.click_btn_add_30)
        self.ui.pushButton_play.clicked.connect(self.start_timer)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogYesButton))
        self.tray_icon.activated.connect(self.restore_window)    

        show_action = QAction("Показати", self)
        show_action.triggered.connect(self.show)
        
        hide_action = QAction("Сховати", self)
        hide_action.triggered.connect(self.hide)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def start_timer(self):
        self.group_off_elem(False)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_timer)
        self.timer.start(1000)

    def show_timer(self):
        s = int(self.ui.label_s.text())
        m = int(self.ui.label_m.text())
        h = int(self.ui.label_h.text())

        if 0 <= s <= 10 and m == 0 and h == 0:
            self.ui.label_s.setStyleSheet("color: red;")
            self.ui.label_m.setStyleSheet("color: red;")
            self.ui.label_h.setStyleSheet("color: red;")

        if s <= 0 and m <= 0 and h <= 0:
            self.timer.stop()
            self.turn_off()
        else:
            all_sec = h_m_in_s(h, m, s)
            all_sec -= 1
            s, m, h = s_in_m_h(all_sec)

            self.ui.label_s.setText(str(add_zero(s)))
            self.ui.label_m.setText(str(add_zero(m)))
            self.ui.label_h.setText(str(add_zero(h)))

    def turn_off(self):
        if self.ui.comboBox_PC_mode.currentText() == "Вимкнути":
            system("shutdown /s /t 0")

        if self.ui.comboBox_PC_mode.currentText() == "Перевантажити":
            system("shutdown /r /t 0")
        
    def change_time(self, elem_name_btn):
        if self.ui.radioButton_s.isChecked():
            if self.ui.comboBox_action_time.currentText() == "Додати":
                self.change_on_time("s", int(elem_name_btn[elem_name_btn.rindex("_") + 1:]), "Додати")
            else:
                self.change_on_time("s", int(elem_name_btn[elem_name_btn.rindex("_") + 1:]), "Відняти")

        if self.ui.radioButton_m.isChecked():
            if self.ui.comboBox_action_time.currentText() == "Додати":
                self.change_on_time("m", int(elem_name_btn[elem_name_btn.rindex("_") + 1:]), "Додати")
            else:
                self.change_on_time("m", int(elem_name_btn[elem_name_btn.rindex("_") + 1:]), "Відняти")

        if self.ui.radioButton_h.isChecked():
            if self.ui.comboBox_action_time.currentText() == "Додати":
                self.change_on_time("h", int(elem_name_btn[elem_name_btn.rindex("_") + 1:]), "Додати")
            else:
                self.change_on_time("h", int(elem_name_btn[elem_name_btn.rindex("_") + 1:]), "Відняти")

    def change_on_time(self, change_time, add_or_vicht_time, operation):
        if operation == "Додати":
            elem_value = int(eval(f"self.ui.label_{change_time}.text()"))
            summ = elem_value + add_or_vicht_time

            eval(f"self.ui.label_{change_time}.setText(str(add_zero({summ})))") if summ < 60 else eval(f'self.ui.label_{change_time}.setText("00")')
        else:
            elem_value = int(eval(f"self.ui.label_{change_time}.text()"))
            summ = elem_value - add_or_vicht_time

            eval(f'self.ui.label_{change_time}.setText("00")') if summ < 0 else eval(f"self.ui.label_{change_time}.setText(str(add_zero({summ})))")

    def click_btn_add_1(self):
        self.change_time(self.ui.pushButton_add_1.objectName())

    def click_btn_add_5(self):
        self.change_time(self.ui.pushButton_add_5.objectName())

    def click_btn_add_10(self):
        self.change_time(self.ui.pushButton_add_10.objectName())
    
    def click_btn_add_20(self):
        self.change_time(self.ui.pushButton_add_20.objectName())

    def click_btn_add_30(self):
        self.change_time(self.ui.pushButton_add_30.objectName())

    def restore_window(self, reason):
        if reason != self.isHidden():              
            self.tray_icon.show()        
            self.showNormal()
        else:
            self.tray_icon.show()        
            self.hide()

    def cancel_timer(self):
        if self.ui.groupBox_2.isEnabled():
            self.msg("Error", "Таймер не було запущено!")
        else:
            self.timer.stop()
            self.msg("Information", f"Таймер '{self.ui.comboBox_PC_mode.currentText()}' ПК скасовано!") 
            self.group_off_elem(True)
            self.reset_time()
            self.ui.label_s.setStyleSheet("color: yellow;")
            self.ui.label_m.setStyleSheet("color: yellow;")
            self.ui.label_h.setStyleSheet("color: yellow;")

    def group_off_elem(self, boolean):
        self.ui.groupBox_2.setEnabled(boolean)
        self.ui.pushButton_play.setEnabled(boolean)
        self.ui.comboBox_PC_mode.setEnabled(boolean)

    def reset_time(self):
        self.ui.label_h.setText("00")
        self.ui.label_m.setText("00")
        self.ui.label_s.setText("00")

    def closeEvent(self, event): 
        if self.ui.pushButton_play.isEnabled():
            QApplication.quit
        else:
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Timer to turn off", "Додаток згорнутий в трей\nПоки таймер не зупинено, Ви не закриєте додаток",
                QSystemTrayIcon.MessageIcon.NoIcon, 
                2000)

    def msg_FAQ_action(self):
        self.msg("Information", "Ви можете додати до (або відняти від) годин(и), хвилин(и), секунд(и)\nвідповідне значення, натиснувши на кнопки з цифрами.")

    def msg_FAQ(self):
        self.msg("Information", f"Щоб скасувати '{self.ui.comboBox_PC_mode.currentText()}' ПК, натисніть кнопку з 'Кошиком'.")    

    def msg(self, reson, message):
        msg = QMessageBox()
        if reson == "Error": 
            msg.setWindowTitle(reson)
            msg.setText(message)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

        if reson == "Information":
            msg.setWindowTitle(reson)
            msg.setText(message)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()