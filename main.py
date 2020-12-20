from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import sqlite3

top = 100
left = 100
width = 700
height = 500

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = QFormLayout(self)
        self.db = 0

        title = "Приложение для показа бд"

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.setFixedSize(width, height)

        # меню
        mainMenu = self.menuBar()
        menu = mainMenu.addMenu("Меню")

        # функция set connection
        setConnection = QAction("Set connection", self)
        setConnection.triggered.connect(self.getConnectionDB)
        menu.addAction(setConnection)

        # функция close connection
        close = QAction("Close", self)
        close.triggered.connect(self.closeConnection)
        menu.addAction(close)

        # кнопка bt1
        self.btn1 = QPushButton("bt1 (select Column)", self)
        self.btn1.move(12,50)
        self.btn1.resize(150,25)
        self.btn1.setFont(QFont('Arial', 7))
        self.btn1.clicked.connect(self.getB1)

        # кнопка bt2
        self.btn2= QPushButton("bt2 (Query2)", self)
        self.btn2.move(174, 50)
        self.btn2.resize(150, 25)
        self.btn2.setFont(QFont('Arial', 7))
        self.btn2.clicked.connect(self.getB2)

        # кнопка bt3
        self.btn3 = QPushButton("bt3 (Query3)", self)
        self.btn3.move(174+150+12, 50)
        self.btn3.resize(150, 25)
        self.btn3.setFont(QFont('Arial', 7))
        self.btn3.clicked.connect(self.getB3)

        # combo box
        self.combo = QComboBox(self)
        self.combo.addItems(['',"date", "name",
                        "power", "age"])
        self.combo.resize(150, 25)
        self.combo.move(174+150+12+200, 50)
        self.combo.currentTextChanged.connect(self.getCombo)

        self.tabs = QTabWidget(self)
        self.tab1 = QTableWidget (self)
        self.tab2 = QTableWidget (self)
        self.tab3 = QTableWidget (self)
        self.tab4 = QTableWidget (self)
        self.tab5 = QTableWidget (self)
        self.tabs.setFixedSize(970, 450)

        # Add tabs
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")
        self.tabs.addTab(self.tab3, "Tab 3")
        self.tabs.addTab(self.tab4, "Tab 4")
        self.tabs.addTab(self.tab5, "Tab 5")
        self.tabs.move(10,100)

    def addTableRow(self, table, row_data):
        row = table.rowCount()
        table.setRowCount(row + 1)
        col = 0
        for item in row_data:
            cell = QTableWidgetItem(str(item))
            table.setItem(row, col, cell)
            col += 1

    def getCombo(self, val):
        if self.db != 0:
            if val != '':
                data = self.db.cursor().execute('SELECT ' + val + ' FROM hero').fetchall()

                self.tab3.setColumnCount(1)
                columnsName = [val]
                self.tab3.rowCount()
                self.tab3.setHorizontalHeaderLabels(columnsName)

                while (self.tab3.rowCount() > 0):
                    self.tab3.removeRow(0)

                for row in data:
                    self.addTableRow(self.tab3, row)
            else:
                while (self.tab3.rowCount() > 0):
                    self.tab3.removeRow(0)
            self.tabs.setCurrentIndex(2)


    def getB1(self):
        if self.db != 0:
            data = self.db.cursor().execute('SELECT date FROM hero').fetchall()

            self.tab2.setColumnCount(1)
            columnsName = ['date']
            self.tab2.rowCount()
            self.tab2.setHorizontalHeaderLabels(columnsName)

            if self.tab2.rowCount() == 0:
                for row in data:
                    self.addTableRow(self.tab2, row)
            self.tabs.setCurrentIndex(1)


    def getB2(self):
        if self.db != 0:
            data = self.db.cursor().execute('SELECT * FROM hero').fetchall()

            info_table = self.db.cursor().execute('PRAGMA table_info(hero)').fetchall()
            self.tab4.setColumnCount(len(info_table))
            columnsName = []
            for row in info_table:
                columnsName.append(row[1])
            self.tab4.rowCount()
            self.tab4.setHorizontalHeaderLabels(columnsName)

            if self.tab4.rowCount() == 0:
                for row in data:
                    self.addTableRow(self.tab4, row)

            self.tabs.setCurrentIndex(3)

    def getB3(self):
        if self.db != 0:
            data = self.db.cursor().execute('SELECT * FROM hero').fetchall()

            info_table = self.db.cursor().execute('PRAGMA table_info(hero)').fetchall()
            self.tab5.setColumnCount(len(info_table))
            columnsName = []
            for row in info_table:
                columnsName.append(row[1])
            self.tab5.rowCount()
            self.tab5.setHorizontalHeaderLabels(columnsName)

            if self.tab5.rowCount() == 0:
                for row in data:
                    self.addTableRow(self.tab5, row)

            self.tabs.setCurrentIndex(4)



    def getConnectionDB(self):
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE if not exists hero
                     (date text, name text, power text, age int)''')
        purchases = [('2020-12-20', 'Iron man', '70', 50),
                     ('2020-12-20', 'Spider-man', '60', 16),
                     ('2020-12-20', 'Halk', '100', 51),
                     ('2020-12-20', 'Tor', '100', 1500)]

        if (c.execute('SELECT count(*) FROM hero').fetchall()[0][0]==0):
            c.executemany('INSERT INTO hero VALUES (?,?,?,?)', purchases)
            conn.commit()

        data = c.execute('SELECT * FROM hero').fetchall()

        info_table = c.execute('PRAGMA table_info(hero)').fetchall()
        self.tab1.setColumnCount(len(info_table))
        columnsName = []
        for row in info_table:
            columnsName.append(row[1])
        self.tab1.rowCount()
        self.tab1.setHorizontalHeaderLabels(columnsName)

        if self.tab1.rowCount() ==0:
            for row in data:
                self.addTableRow(self.tab1, row)

        self.tabs.setCurrentIndex(0)
        self.db = conn

    def closeConnection(self):
        if self.db != 0:
            while (self.tab1.rowCount() > 0):
                self.tab1.removeRow(0)
            self.tab1.setColumnCount(0)

            while (self.tab2.rowCount() > 0):
                self.tab2.removeRow(0)
            self.tab2.setColumnCount(0)

            while (self.tab3.rowCount() > 0):
                self.tab3.removeRow(0)
            self.tab3.setColumnCount(0)

            while (self.tab4.rowCount() > 0):
                self.tab4.removeRow(0)
            self.tab4.setColumnCount(0)

            while (self.tab5.rowCount() > 0):
                self.tab5.removeRow(0)
            self.tab5.setColumnCount(0)

            self.db.close()
            self.db = 0
            
    def closeEvent(self, event):
        print("auto close connection")
        self.closeConnection()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()