import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QListWidget, QComboBox, QMessageBox, QDateTimeEdit, QCalendarWidget, QTimeEdit
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QColor, QFont, QIcon


class ToDoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List")
        self.setGeometry(100, 100, 500, 650)

        # Lista de tareas
        self.tasks = []

        # Widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Campo de texto para agregar tareas
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Escribe una tarea...")
        self.task_input.setStyleSheet("padding: 5px; border: 2px solid #4CAF50; border-radius: 5px;")
        self.main_layout.addWidget(self.task_input)

        # Selector de categoría
        self.category_selector = QComboBox()
        self.category_selector.addItem("Importante")
        self.category_selector.addItem("Normal")
        self.category_selector.addItem("Tareas Pendientes")
        self.category_selector.setStyleSheet("padding: 5px; border: 2px solid #4CAF50; border-radius: 5px;")
        self.main_layout.addWidget(self.category_selector)

        # Selector de fecha y hora de expiración
        self.expiration_datetime = QDateTimeEdit(QDateTime.currentDateTime())
        self.expiration_datetime.setDisplayFormat("dd/MM/yyyy hh:mm")
        self.expiration_datetime.setStyleSheet("padding: 5px; border: 2px solid #4CAF50; border-radius: 5px;")
        self.main_layout.addWidget(self.expiration_datetime)

        # Botón para agregar tareas
        self.add_button = QPushButton("Agregar Tarea")
        self.add_button.clicked.connect(self.add_task)
        self.add_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; border-radius: 5px;")
        self.main_layout.addWidget(self.add_button)

        # Lista para mostrar las tareas
        self.task_list = QListWidget()
        self.task_list.setStyleSheet("background-color: #f4f4f4; color: #333; padding: 5px; border-radius: 5px;")
        self.main_layout.addWidget(self.task_list)

        # Botón para eliminar tareas seleccionadas
        self.delete_button = QPushButton("Eliminar Tarea")
        self.delete_button.clicked.connect(self.delete_task)
        self.delete_button.setStyleSheet("background-color: #f44336; color: white; padding: 5px; border-radius: 5px;")
        self.main_layout.addWidget(self.delete_button)

    def add_task(self):
        task_text = self.task_input.text().strip()
        if task_text:
            category = self.category_selector.currentText()
            if isinstance(self.expiration_datetime, QDateTimeEdit):
                expiration = self.expiration_datetime.dateTime().toString("dd/MM/yyyy hh:mm")
            elif isinstance(self.expiration_datetime, QCalendarWidget):
                expiration = self.expiration_datetime.selectedDate().toString("dd/MM/yyyy")
            elif isinstance(self.expiration_datetime, QTimeEdit):
                expiration = self.expiration_datetime.time().toString("hh:mm")
            task = {"text": task_text, "category": category, "expiration": expiration}
            self.tasks.append(task)
            self.task_input.clear()
            self.update_task_list()

    def delete_task(self):
        selected_task = self.task_list.currentRow()
        if selected_task != -1:
            del self.tasks[selected_task]
            self.update_task_list()
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona una tarea para eliminar.")

    def update_task_list(self):
        self.task_list.clear()
        for task in self.tasks:
            self.task_list.addItem(f"{task['text']} - {task['category']} - Expira en: {task['expiration']}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())
