import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QListWidget, QComboBox, QMessageBox, QDateTimeEdit
from PyQt5.QtCore import QDateTime

# Aplicación To-Do
class ToDoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List")
        self.setGeometry(100, 100, 500, 650)

        self.tasks = []

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Escribe una tarea...")
        self.main_layout.addWidget(self.task_input)

        self.category_selector = QComboBox()
        self.category_selector.addItem("Importante")
        self.category_selector.addItem("Normal")
        self.category_selector.addItem("Tareas Pendientes")
        self.main_layout.addWidget(self.category_selector)

        self.expiration_datetime = QDateTimeEdit(QDateTime.currentDateTime())
        self.expiration_datetime.setDisplayFormat("dd/MM/yyyy hh:mm")
        self.main_layout.addWidget(self.expiration_datetime)

        self.add_button = QPushButton("Agregar Tarea")
        self.add_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        self.add_button.clicked.connect(self.add_task)
        self.main_layout.addWidget(self.add_button)

        self.task_list = QListWidget()
        self.task_list.setStyleSheet("background-color: #f9f9f9; font-size: 14px;")
        self.main_layout.addWidget(self.task_list)

        self.delete_button = QPushButton("Eliminar Tarea")
        self.delete_button.setStyleSheet("background-color: #f44336; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        self.delete_button.clicked.connect(self.delete_task)
        self.main_layout.addWidget(self.delete_button)

        self.load_tasks()

    def add_task(self):
        task_text = self.task_input.text().strip()
        if task_text:
            category = self.category_selector.currentText()
            expiration = self.expiration_datetime.dateTime().toString("dd/MM/yyyy hh:mm")
            task = {"text": task_text, "category": category, "expiration": expiration}
            self.tasks.append(task)
            self.task_input.clear()
            self.update_task_list()
            self.save_tasks()

    def delete_task(self):
        selected_task = self.task_list.currentRow()
        if selected_task != -1:
            del self.tasks[selected_task]
            self.update_task_list()
            self.save_tasks()
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona una tarea para eliminar.")

    def update_task_list(self):
        self.task_list.clear()
        for task in self.tasks:
            self.task_list.addItem(f"{task['text']} - {task['category']} - Expira en: {task['expiration']}")

    def save_tasks(self):
        with open('tasks.json', 'w') as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as f:
                self.tasks = json.load(f)
                self.update_task_list()
        except FileNotFoundError:
            self.tasks = []

if __name__ == "__main__":
    app = QApplication(sys.argv)

    style_sheet = """
        QWidget {
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
        }
        QLineEdit, QPushButton, QComboBox {
            margin: 10px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        QListWidget {
            background-color: #ffffff;
            border: 1px solid #ddd;
        }
        QPushButton {
            font-size: 16px;
        }
    """
    app.setStyleSheet(style_sheet)

    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())
