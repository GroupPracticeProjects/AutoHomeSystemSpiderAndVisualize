from PyQt5.QtCore import pyqtSlot, QSize, Qt, QModelIndex, QSortFilterProxyModel
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QHeaderView
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from Ui__mainUI import Ui_MainWindow


class Mcar(QMainWindow, Ui_MainWindow):
    """
    汽车参数数据管理
    """
    sqlModel = QSqlQueryModel()

    def __init__(self, db, parent=None):
        """
        设置表格样式
        """
        super(Mcar, self).__init__(parent)
        self.setupUi(self)
        self.db = db
        self.initUi()

    def initUi(self):
        # 左右分栏布局五五开
        self.splitter.setStretchFactor(0, 5)
        self.splitter.setStretchFactor(1, 5)

        query = QSqlQuery()

        # 系列复选框关键字(遍历)
        series_key = ["", ]
        query.exec_("SELECT 系列 from CarData group by 系列;")
        while (query.next()):
            series_key.append(query.value(0))
        self.comboBox.addItems(series_key)

        # 级别复选框关键字
        level_key = ["", ]
        query.exec_("SELECT 级别 from CarData group by 级别;")
        while (query.next()):
            level_key.append(query.value(0))
        self.comboBox_3.addItems(level_key)

        # 价格复选框关键字
        price_key = ["", "厂商指导价", "补贴售后价", "经销商参考价"]
        self.comboBox_2.addItems(price_key)

        # 能源类型关键字
        energytype_key = ["", ]
        query.exec_("SELECT 能源类型 from CarData group by 能源类型;")
        while (query.next()):
            energytype_key.append(query.value(0))
        self.comboBox_4.addItems(energytype_key)

        # 厂商关键字
        vendertype_key = ["", ]
        query.exec_("SELECT 厂商 from CarData group by 厂商;")
        while (query.next()):
            vendertype_key.append(query.value(0))
        self.comboBox_5.addItems(vendertype_key)

        # 环保标准关键字
        envstandard_key = ["", ]
        query.exec_("SELECT 环保标准 from CarData group by 环保标准;")
        while (query.next()):
            envstandard_key.append(query.value(0))
        self.comboBox_6.addItems(envstandard_key)

        self.tableView.setIconSize(QSize(55, 25))
        # 水平布局填充
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.setTableModel()

    def loading(self):
        while self.sqlModel.canFetchMore():
            self.sqlModel.fetchMore()

    def setTableModel(self):
        """
        表格数据显示
        """
        # self.sqlModel = QSqlQueryModel()
        # self.sqlModel.setQuery("SELECT * FROM CarData;")
        self.sqlModel.setQuery("SELECT id,系列,车型,厂商指导价,补贴后售价,经销商参考价,厂商,级别,能源类型,环保标准,上市时间,\"最大功率(kW)\",\"最大扭矩(N·m)\",发动机,变速箱,\"长*宽*高(mm)\",车身结构,\"最高车速(km/h)\",\"官方0-100km/h加速(s)\",\"实测0-100km/h加速(s)\",\"实测100-0km/h制动(m)\",\"工信部综合油耗(L/100km)\",\"实测油耗(L/100km)\",整车质保,\"长度(mm)\",\"宽度(mm)\",\"高度(mm)\",\"轴距(mm)\",\"前轮距(mm)\",\"后轮距(mm)\",\"最小离地间隙(mm)\",\"车门数(个)\",\"座位数(个)\",\"油箱容积(L)\",\"行李厢容积(L)\",\"整备质量(kg)\",发动机型号,\"排量(mL)\",\"排量(L)\",进气形式 FROM CarData;")
        print("数据库读取中.....")
        # while self.sqlModel.canFetchMore():
        #     self.sqlModel.fetchMore()
        self.proxyModel = QSortFilterProxyModel()
        # self.proxyModel.sort(0, Qt.AscendingOrder) 会有bug
        self.proxyModel.setSourceModel(self.sqlModel)
        # 大小写不敏感
        self.proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.tableView.setModel(self.proxyModel)
        # 开启排序
        # self.tableView.setSortingEnabled(True)
        self.tableView.hideColumn(0)
        # hidden
        for i in range(8, 1371):
            self.tableView.hideColumn(i)
        # self.tableView.show()

    @pyqtSlot(QModelIndex)
    def on_tableView_clicked(self, index):
        """
        单击显示车辆详细信息
        """
        row = index.row()
        self.label_12.setText(self.sqlModel.record(row).value("系列"))
        self.label_14.setText(self.sqlModel.record(row).value("车型"))
        strp1 = str(self.sqlModel.record(row).value("厂商指导价"))
        if strp1 != "暂无报价":
            self.label_16.setText(strp1+"万元")
        else:
            self.label_16.setText("暂无报价")
        strp2 = str(self.sqlModel.record(row).value("补贴后售价"))
        if strp2 != "暂无报价":
            self.label_18.setText(strp2 + "万元")
        else:
            self.label_18.setText("暂无报价")
        strp3 = str(self.sqlModel.record(row).value("经销商参考价"))
        if strp3 != "暂无报价":
            self.label_20.setText(strp3 + "万元")
        else:
            self.label_20.setText("暂无报价")
        self.label_22.setText(self.sqlModel.record(row).value("厂商"))
        self.label_24.setText(self.sqlModel.record(row).value("级别"))
        self.label_26.setText(self.sqlModel.record(row).value("能源类型"))
        self.label_28.setText(self.sqlModel.record(row).value("环保标准"))
        self.label_30.setText(str(self.sqlModel.record(row).value("上市时间")))
        self.label_32.setText(str(self.sqlModel.record(row).value("最大功率(kW)")))
        self.label_34.setText(str(self.sqlModel.record(row).value("最大扭矩(N·m)")))
        self.label_36.setText(self.sqlModel.record(row).value("发动机"))
        self.label_38.setText(self.sqlModel.record(row).value("变速箱"))
        self.label_40.setText(self.sqlModel.record(row).value("长*宽*高(mm)"))
        self.label_42.setText(self.sqlModel.record(row).value("车身结构"))
        self.label_44.setText(str(self.sqlModel.record(row).value("最高车速(km/h)")))
        self.label_46.setText(str(self.sqlModel.record(row).value("官方0-100km/h加速(s)")))
        self.label_48.setText(str(self.sqlModel.record(row).value("实测0-100km/h加速(s)")))
        self.label_50.setText(str(self.sqlModel.record(row).value("实测100-0km/h制动(m)")))
        self.label_52.setText(str(self.sqlModel.record(row).value("工信部综合油耗(L/100km)")))
        self.label_54.setText(str(self.sqlModel.record(row).value("实测油耗(L/100km)")))
        self.label_56.setText(self.sqlModel.record(row).value("整车质保"))
        self.label_58.setText(self.sqlModel.record(row).value("进气形式"))
        self.label_60.setText(str(self.sqlModel.record(row).value("车门数(个)")))
        self.label_70.setText(str(self.sqlModel.record(row).value("排量(L)")))
        self.label_62.setText(str(self.sqlModel.record(row).value("座位数(个)")))
        self.label_64.setText(str(self.sqlModel.record(row).value("油箱容积(L)")))
        self.label_66.setText(str(self.sqlModel.record(row).value("行李厢容积(L)")))
        self.label_68.setText(self.sqlModel.record(row).value("发动机型号"))

    @pyqtSlot()
    def on_pushButton_search_clicked(self):
        # 系列
        self.seriesFilter = self.comboBox.currentText()
        # 级别
        self.levelFilter = self.comboBox_3.currentText()
        # 价格
        self.priceFilter = self.comboBox_2.currentText()
        # 能源类型
        self.energyFilter = self.comboBox_4.currentText()
        # 厂商
        self.vendorFilter = self.comboBox_5.currentText()
        # 环保标准
        self.envFilter = self.comboBox_6.currentText()
        # 价格下限
        self.bottomFilter = self.lineEdit_bottomPrice.text()
        # 价格上限
        self.topFilter = self.lineEdit_topPrice.text()
        self.Filter(self.seriesFilter, self.levelFilter, self.priceFilter, self.energyFilter, self.vendorFilter,
                    self.envFilter, self.bottomFilter, self.topFilter)


    def Filter(self, sf, lf, pf, enef, vf, envf, bf, tf):
        for i in range(8, 1371):
            self.tableView.hideColumn(i)
        if sf == lf == pf == enef == vf == envf == bf == tf == self.lineEdit.text() == self.lineEdit_2.text() == self.lineEdit_topPrice.text() == self.lineEdit_bottomPrice.text() == "":
            self.sqlModel.setQuery(
                "SELECT id,系列,车型,厂商指导价,补贴后售价,经销商参考价,厂商,级别,能源类型,环保标准,上市时间,\"最大功率(kW)\",\"最大扭矩(N·m)\",发动机,变速箱,\"长*宽*高(mm)\",车身结构,\"最高车速(km/h)\",\"官方0-100km/h加速(s)\",\"实测0-100km/h加速(s)\",\"实测100-0km/h制动(m)\",\"工信部综合油耗(L/100km)\",\"实测油耗(L/100km)\",整车质保,\"长度(mm)\",\"宽度(mm)\",\"高度(mm)\",\"轴距(mm)\",\"前轮距(mm)\",\"后轮距(mm)\",\"最小离地间隙(mm)\",\"车门数(个)\",\"座位数(个)\",\"油箱容积(L)\",\"行李厢容积(L)\",\"整备质量(kg)\",发动机型号,\"排量(mL)\",\"排量(L)\",进气形式 FROM CarData;")
        elif pf == "" and (self.lineEdit_topPrice.text() != "" or self.lineEdit_bottomPrice.text() != ""):
            msg_box = QMessageBox()
            msg_box.setWindowTitle("提示")
            msg_box.setText("请选择价格")
            if msg_box.exec_() == QMessageBox.Yes:
                return
        else:
            arr = {'系列': sf, '级别': lf, '能源类型': enef, '厂商': vf, '环保标准': envf}
            base_query = "SELECT id,系列,车型,厂商指导价,补贴后售价,经销商参考价,厂商,级别,能源类型,环保标准,上市时间,\"最大功率(kW)\",\"最大扭矩(N·m)\",发动机,变速箱,\"长*宽*高(mm)\",车身结构,\"最高车速(km/h)\",\"官方0-100km/h加速(s)\",\"实测0-100km/h加速(s)\",\"实测100-0km/h制动(m)\",\"工信部综合油耗(L/100km)\",\"实测油耗(L/100km)\",整车质保,\"长度(mm)\",\"宽度(mm)\",\"高度(mm)\",\"轴距(mm)\",\"前轮距(mm)\",\"后轮距(mm)\",\"最小离地间隙(mm)\",\"车门数(个)\",\"座位数(个)\",\"油箱容积(L)\",\"行李厢容积(L)\",\"整备质量(kg)\",发动机型号,\"排量(mL)\",\"排量(L)\",进气形式 FROM CarData WHERE "
            # base_query = "SELECT * FROM CarData WHERE "
            flag = True
            for key in arr.keys():
                if arr[key] != "" and flag:
                    flag = False
                    base_query = base_query + key + "=" + '\"' + arr[key] + '\"'
                elif not flag and arr[key] != "":
                    base_query = base_query + " AND " + key + "=" + '\"' + arr[key] + '\"'

            # 上市时间筛选
            if self.lineEdit.text() != "" and self.lineEdit_2.text() != "" and flag:
                flag = False
                base_query = base_query + "\"上市时间\" BETWEEN " + self.lineEdit.text() + " AND " + self.lineEdit_2.text()
            elif self.lineEdit.text() != "" and self.lineEdit_2.text() != "" and (not flag):
                base_query = base_query + " AND " + "\"上市时间\" BETWEEN " + self.lineEdit.text() + " AND " + self.lineEdit_2.text()
            # 价格筛选
            if self.lineEdit_bottomPrice.text() != "" and self.lineEdit_topPrice.text() != "" and pf != "" and flag:
                flag = False
                base_query = base_query + "\"" + pf + "\"" + " BETWEEN " + self.lineEdit_bottomPrice.text() + " AND " + self.lineEdit_topPrice.text()
            elif self.lineEdit_bottomPrice.text() != "" and self.lineEdit_topPrice.text() != "" and pf != "" and (not flag):
                base_query = base_query + " AND " + "\"" + pf + "\"" + " BETWEEN " + self.lineEdit_bottomPrice.text() + " AND " + self.lineEdit_topPrice.text()
            base_query = base_query + " ORDER BY " + "id" + ';'
            self.sqlModel.setQuery(base_query)