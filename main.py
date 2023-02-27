from sys import exit, argv

from PyQt6.QtWidgets import QApplication

from GUI import MainWindow

def main():
    app = QApplication(argv)
    appl = MainWindow()
    appl.show()

    try:
        exit(app.exec())
    except:
        pass

if __name__ == "__main__":
    main()