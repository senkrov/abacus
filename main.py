import sys
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit
from PyQt6.QtCore import Qt
from ui.abacus_widget import AbacusWidget

class AbacusWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Abacus Calculator")
        self.setGeometry(100, 100, 800, 600) # Adjust size as needed

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Value display at the top
        self.value_display = QLineEdit()
        self.value_display.setReadOnly(True) # Make it read-only
        self.value_display.setAlignment(Qt.AlignmentFlag.AlignRight) # Align text to the right
        self.value_display.setStyleSheet("font-size: 30px; padding: 5px;") # Style it
        layout.addWidget(self.value_display)

        self.abacus_widget = AbacusWidget()
        layout.addWidget(self.abacus_widget)

        # Connect the abacus widget's valueChanged signal to update the display
        self.abacus_widget.valueChanged.connect(self.update_value_display)

        # Initialize display with current abacus value
        self.update_value_display(self.abacus_widget.abacus.get_value())

        self.show()

    def update_value_display(self, value):
        self.value_display.setText(str(value))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AbacusWindow()
    sys.exit(app.exec())
