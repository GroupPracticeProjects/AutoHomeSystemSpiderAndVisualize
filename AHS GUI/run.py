from mcar import Mcar
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtSql import QSqlDatabase
import sys, os


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = sys.MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def connectDB(resource_path):
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(resource_path)
    if not db.open():
        QMessageBox.critical(None, "严重错误", "数据连接失败，程序无法使用，请按取消键退出", QMessageBox.Cancel)
        return  False
    else:
        return db

if __name__=="__main__":
    app = QApplication(sys.argv)
    filepath = resource_path(os.path.join("res", "autohome.db"))
    print(filepath)
    db = connectDB(filepath)
    if db:
        mc = Mcar(db)
        mc.show()
        Mcar.loading(self=mc)
        sys.exit(app.exec_())