import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QTableWidgetItem
)
from PyQt5.uic import loadUi

from models.item_model import (
    get_all_items, add_item, update_item, delete_item, search_items)
from models.category_model import get_categories
from models.supplier_model import get_suppliers


class InventoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/main_window.ui", self)
        self.load_items()
        self.load_categories()
        self.load_suppliers()

        # Connect buttons
        self.btnAdd.clicked.connect(self.add_item)
        self.btnUpdate.clicked.connect(self.update_selected_item)
        self.btnDelete.clicked.connect(self.delete_selected_item)
        self.btnRefresh.clicked.connect(self.load_items)
        self.btnSearch.clicked.connect(self.search_items)

        # Connect table click
        self.tblItems.cellClicked.connect(self.fill_form_from_selection)

        self.selected_item_id = None

    def load_items(self):
        self.tblItems.setRowCount(0)
        for row_data in get_all_items():
            self._add_row(row_data)

    def load_categories(self):
        self.cmbCategory.clear()
        for id, name in get_categories():
            self.cmbCategory.addItem(name, id)

    def load_suppliers(self):
        self.cmbSupplier.clear()
        for id, name in get_suppliers():
            self.cmbSupplier.addItem(name, id)

    def add_item(self):
        name = self.txtName.text()
        category_id = self.cmbCategory.currentData()
        supplier_id = self.cmbSupplier.currentData()
        quantity = self.spnQuantity.value()

        if name.strip() == "":
            QMessageBox.warning(self, "Input Error", "Item name is required.")
            return

        add_item(name, category_id, supplier_id, quantity)
        QMessageBox.information(self, "Success", "Item added successfully.")
        self.clear_form()
        self.load_items()

    def fill_form_from_selection(self, row, column):
        self.selected_item_id = int(self.tblItems.item(row, 0).text())
        self.txtName.setText(self.tblItems.item(row, 1).text())
        self.spnQuantity.setValue(int(self.tblItems.item(row, 4).text()))

        category_name = self.tblItems.item(row, 2).text()
        supplier_name = self.tblItems.item(row, 3).text()

        index_cat = self.cmbCategory.findText(category_name)
        index_sup = self.cmbSupplier.findText(supplier_name)
        if index_cat != -1:
            self.cmbCategory.setCurrentIndex(index_cat)
        if index_sup != -1:
            self.cmbSupplier.setCurrentIndex(index_sup)

    def update_selected_item(self):
        if not self.selected_item_id:
            QMessageBox.warning(self, "Select Item", "Please select an item to update.")
            return

        name = self.txtName.text()
        category_id = self.cmbCategory.currentData()
        supplier_id = self.cmbSupplier.currentData()
        quantity = self.spnQuantity.value()

        update_item(self.selected_item_id, name, category_id, supplier_id, quantity)
        QMessageBox.information(self, "Updated", "Item updated successfully.")
        self.clear_form()
        self.load_items()

    def delete_selected_item(self):
        if not self.selected_item_id:
            QMessageBox.warning(self, "Select Item", "Please select an item to delete.")
            return

        confirm = QMessageBox.question(
            self, "Confirm Delete", "Are you sure you want to delete this item?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_item(self.selected_item_id)
            QMessageBox.information(self, "Deleted", "Item deleted successfully.")
            self.clear_form()
            self.load_items()

    def search_items(self):
        keyword = self.txtSearch.text()
        self.tblItems.setRowCount(0)
        for row_data in search_items(keyword):
            self._add_row(row_data)

    def clear_form(self):
        self.txtName.clear()
        self.spnQuantity.setValue(0)
        self.cmbCategory.setCurrentIndex(0)
        self.cmbSupplier.setCurrentIndex(0)
        self.selected_item_id = None
        self.tblItems.clearSelection()

    def _add_row(self, row_data):
        row = self.tblItems.rowCount()
        self.tblItems.insertRow(row)
        for col, data in enumerate(row_data):
            self.tblItems.setItem(row, col, QTableWidgetItem(str(data)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.setWindowTitle("Inventory Management System")
    window.show()
    sys.exit(app.exec_())

