from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMessageBox
from app.inventory import get_inventory, add_inventory, update_inventory, delete_inventory
from app.category import get_all_categories
from app.supplier import get_all_suppliers
import sys

class InventoryApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(InventoryApp, self).__init__()
        uic.loadUi("../ui/main_window.ui", self)

        self.load_categories()
        self.load_suppliers()
        self.load_inventory()

        self.searchInput.textChanged.connect(self.load_inventory)
        self.categoryFilter.currentIndexChanged.connect(self.load_inventory)
        self.supplierFilter.currentIndexChanged.connect(self.load_inventory)
        self.addButton.clicked.connect(self.add_item)
        self.updateButton.clicked.connect(self.update_item)
        self.deleteButton.clicked.connect(self.delete_item)
        self.inventoryTable.itemSelectionChanged.connect(self.fill_form)

    def load_categories(self):
        categories = get_all_categories()
        self.categoryCombo.clear()
        self.categoryFilter.clear()
        self.categoryCombo.addItem("Select Category", -1)
        self.categoryFilter.addItem("All Categories", -1)
        for cat in categories:
            self.categoryCombo.addItem(cat[1], cat[0])
            self.categoryFilter.addItem(cat[1], cat[0])

    def load_suppliers(self):
        suppliers = get_all_suppliers()
        self.supplierCombo.clear()
        self.supplierFilter.clear()
        self.supplierCombo.addItem("Select Supplier", -1)
        self.supplierFilter.addItem("All Suppliers", -1)
        for sup in suppliers:
            self.supplierCombo.addItem(sup[1], sup[0])
            self.supplierFilter.addItem(sup[1], sup[0])

    def load_inventory(self):
        search_text = self.searchInput.text().strip()
        category_id = self.categoryFilter.currentData()
        supplier_id = self.supplierFilter.currentData()
        data = get_inventory(search_text, category_id, supplier_id)

        self.inventoryTable.setRowCount(0)
        for row_data in data:
            row = self.inventoryTable.rowCount()
            self.inventoryTable.insertRow(row)
            for col, value in enumerate(row_data):
                self.inventoryTable.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))

            if row_data[4] < 5:
                for col in range(6):
                    self.inventoryTable.item(row, col).setBackground(QtCore.Qt.red)

    def add_item(self):
        name = self.nameInput.text()
        category_id = self.categoryCombo.currentData()
        supplier_id = self.supplierCombo.currentData()
        quantity = self.quantitySpin.value()
        price = self.priceSpin.value()

        if category_id == -1 or supplier_id == -1 or not name:
            QMessageBox.warning(self, "Validation Error", "Please fill all fields.")
            return

        add_inventory(name, category_id, supplier_id, quantity, price)
        self.load_inventory()
        self.clear_inputs()

    def update_item(self):
        selected = self.inventoryTable.selectedItems()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select an item to update.")
            return

        item_id = int(selected[0].text())
        name = self.nameInput.text()
        category_id = self.categoryCombo.currentData()
        supplier_id = self.supplierCombo.currentData()
        quantity = self.quantitySpin.value()
        price = self.priceSpin.value()

        update_inventory(item_id, name, category_id, supplier_id, quantity, price)
        self.load_inventory()
        self.clear_inputs()

    def delete_item(self):
        selected = self.inventoryTable.selectedItems()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select an item to delete.")
            return

        item_id = int(selected[0].text())
        confirm = QMessageBox.question(self, "Confirm Delete", f"Delete item {item_id}?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            delete_inventory(item_id)
            self.load_inventory()
            self.clear_inputs()

    def fill_form(self):
        selected = self.inventoryTable.selectedItems()
        if not selected:
            return
        self.nameInput.setText(selected[1].text())
        self.categoryCombo.setCurrentText(selected[2].text())
        self.supplierCombo.setCurrentText(selected[3].text())
        self.quantitySpin.setValue(int(selected[4].text()))
        self.priceSpin.setValue(float(selected[5].text()))

    def clear_inputs(self):
        self.nameInput.clear()
        self.categoryCombo.setCurrentIndex(0)
        self.supplierCombo.setCurrentIndex(0)
        self.quantitySpin.setValue(0)
        self.priceSpin.setValue(0.0)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec_())
