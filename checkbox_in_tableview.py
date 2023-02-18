import sys
from PyQt5.QtSql import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MyButtonDelegate(QStyledItemDelegate):#自定义的委托控件checkbox
    def __init__(self, parent=None):
        super(MyButtonDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            
            checkbox = QCheckBox('')
            checkbox.toggled.connect(lambda:self.parent().btnstate(checkbox))
            
            checkbox.index = [index.row(), index.column()]
            
            h_box_layout = QHBoxLayout()
            h_box_layout.addWidget(checkbox)
            #h_box_layout.addWidget(button_write)
            h_box_layout.setContentsMargins(0, 0, 0, 0)
            h_box_layout.setAlignment(Qt.AlignCenter)
            widget = QWidget()
            widget.setLayout(h_box_layout)
            self.parent().setIndexWidget(
                index,
                widget
            )

class MyTableView(QTableView):
    def __init__(self, parent=None):
        super(MyTableView, self).__init__(parent)
        #将自定义的委托控件植入tableview中
        self.setItemDelegateForColumn(0, MyButtonDelegate(self))
        self.row = []

    def cellButtonClicked(self):
        print("Cell Button Clicked", self.sender().index)

    def btnstate(self,b):
        if b.isChecked() == True:
            print('选中')
            self.row.append(self.sender().index[0])
        else:
            print('取消选择')
        #print("Cell Button Clicked", self.sender().index)
        
        
def initializeModel(model):
   model.setTable('todo')
   model.setEditStrategy(QSqlTableModel.OnFieldChange)
   model.select()
   model.setHeaderData(0, Qt.Horizontal, "状态")
   model.setHeaderData(1, Qt.Horizontal, "点位")
   model.setHeaderData(2, Qt.Horizontal, "内容")
   model.setHeaderData(3, Qt.Horizontal, "周期")
   model.setHeaderData(4, Qt.Horizontal, "到期时间")

def createView(title, model):
   view = MyTableView()
   view.setModel(model)
   view.setWindowTitle(title)
   return view

def addrow():
   print (model.rowCount())
   ret = model.insertRows(model.rowCount(), 1)
   print (ret)

def findrow(i):
   delrow = i.row()

def delrows(model, rows):
    for current_row in rows:
        model.removeRow(current_row)       

if __name__ == '__main__':
   app = QApplication(sys.argv)
   db = QSqlDatabase.addDatabase('QSQLITE')
   db.setDatabaseName('wtd.db')
   model = QSqlTableModel()
   delrow = -1
   initializeModel(model)

   view1 = createView("Table Model (View 1)", model)
   view1.clicked.connect(findrow)

   dlg = QDialog()
   layout = QVBoxLayout()
   layout.addWidget(view1)

   button = QPushButton("Add a row")
   button.clicked.connect(addrow)
   layout.addWidget(button)

   btn1 = QPushButton("del a row")
   btn1.clicked.connect(lambda:delrows(model,view1.row))
   layout.addWidget(btn1)

   dlg.setLayout(layout)
   dlg.setWindowTitle("Database Demo")
   dlg.show()
   sys.exit(app.exec_())