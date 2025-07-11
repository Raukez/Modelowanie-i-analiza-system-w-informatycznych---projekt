import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QDialog,
                             QLineEdit, QFormLayout, QDialogButtonBox,
                             QFrame, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter, QPen
from PyQt5.QtWidgets import QFrame


class InputDialog(QDialog):
    def __init__(self, title, label1, label2, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)

        layout = QVBoxLayout()

        # Formularz
        form_layout = QFormLayout()
        self.input1 = QLineEdit()
        self.input2 = QLineEdit()

        form_layout.addRow(f"{label1}:", self.input1)
        form_layout.addRow(f"{label2}:", self.input2)

        layout.addLayout(form_layout)

        # Przyciski
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_values(self):
        return self.input1.text(), self.input2.text()


class InputDialog2(QDialog):
    def __init__(self, title, label1, label2, label3, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)

        layout = QVBoxLayout()

        # Formularz
        form_layout = QFormLayout()
        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        self.input3 = QLineEdit()

        form_layout.addRow(f"{label1}:", self.input1)
        form_layout.addRow(f"{label2}:", self.input2)
        form_layout.addRow(f"{label3}:", self.input3)

        layout.addLayout(form_layout)

        # Przyciski
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_values(self):
        return self.input1.text(), self.input2.text(), self.input3.text()


class ArcDisplay(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self.display_text = text
        self.setMinimumHeight(80)
        self.setStyleSheet("border: 1px solid black; background-color: white;")

    def set_text(self, text):
        self.display_text = text
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.display_text:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            rect = self.rect()
            arc_rect = rect.adjusted(100, 40, -100, -30)

            pen = QPen(Qt.black, 2)
            painter.setPen(pen)

            painter.drawArc(arc_rect, 0, 180 * 16)

            font = QFont()
            font.setPointSize(16)
            painter.setFont(font)

            text_rect = rect.adjusted(0, 35, 0, 0)
            painter.drawText(text_rect, Qt.AlignCenter, self.display_text)


class LineDisplay(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self.display_text = text
        self.setMinimumHeight(80)
        self.setStyleSheet("border: 1px solid black; background-color: white;")

    def set_text(self, text):
        self.display_text = text
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.display_text:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            rect = self.rect()

            pen = QPen(Qt.black, 2)
            painter.setPen(pen)

            font = QFont()
            font.setPointSize(16)
            painter.setFont(font)

            metrics = painter.fontMetrics()
            text_width = metrics.horizontalAdvance(self.display_text) + 50

            center_x = rect.width() // 2
            line_start = center_x - text_width // 2
            line_end = center_x + text_width // 2

            line_y = rect.height() // 3
            painter.drawLine(line_start, line_y, line_end, line_y)

            painter.drawLine(line_start, line_y - 5, line_start, line_y + 5)
            painter.drawLine(line_end, line_y - 5, line_end, line_y + 5)

            text_rect = rect.adjusted(0, 25, 0, 0)
            painter.drawText(text_rect, Qt.AlignCenter, self.display_text)


class ComplexDisplay(QLabel):
    def __init__(self, text="", display_type="arc_line", parent=None):
        super().__init__(parent)
        self.display_text = text
        self.display_type = display_type
        self.setMinimumHeight(80)
        self.setStyleSheet("border: 1px solid black; background-color: white;")

    def set_text(self, text, display_type="arc_line"):
        self.display_text = text
        self.display_type = display_type
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.display_text:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            rect = self.rect()
            pen = QPen(Qt.black, 2)
            painter.setPen(pen)

            font = QFont()
            font.setPointSize(14)
            painter.setFont(font)

            metrics = painter.fontMetrics()

            if self.display_type == "arc_line":
                parts = self.display_text.split(';')
                if len(parts) >= 3:
                    left_part = parts[0].strip() + " ; " + parts[1].strip()
                    right_part = parts[2].strip()

                    left_width = metrics.horizontalAdvance(left_part)
                    right_width = metrics.horizontalAdvance(right_part)

                    total_text_width = metrics.horizontalAdvance(self.display_text)
                    text_start = (rect.width() - total_text_width) // 2

                    left_start_pos = text_start
                    left_end_pos = left_start_pos + left_width

                    spaces_width = metrics.horizontalAdvance("     ")
                    right_start_pos = left_end_pos + spaces_width
                    right_end_pos = right_start_pos + right_width

                    line_y = rect.height() // 4

                    painter.drawLine(left_start_pos, line_y, right_end_pos + 10, line_y)
                    painter.drawLine(left_start_pos, line_y - 5, left_start_pos, line_y + 5)
                    painter.drawLine(right_end_pos + 10, line_y - 5, right_end_pos + 10, line_y + 5)

                    left_center = (left_start_pos + left_end_pos) // 2
                    arc_width = left_width
                    arc_rect = rect.adjusted(left_center - arc_width // 2, 55,
                                             -rect.width() + left_center + arc_width // 2, -80)
                    painter.drawArc(arc_rect, 0, 180 * 16)

            else:
                parts = self.display_text.split(';')
                if len(parts) >= 3:
                    left_part = parts[0].strip()
                    right_part = parts[1].strip() + " ; " + parts[2].strip()

                    left_width = metrics.horizontalAdvance(left_part)
                    right_width = metrics.horizontalAdvance(right_part)

                    total_text_width = metrics.horizontalAdvance(self.display_text)
                    text_start = (rect.width() - total_text_width) // 2

                    left_start_pos = text_start
                    left_end_pos = left_start_pos + left_width

                    spaces_width = metrics.horizontalAdvance(" ;     ")
                    right_start_pos = left_end_pos + spaces_width
                    right_end_pos = right_start_pos + right_width

                    line_y = rect.height() // 4

                    painter.drawLine(left_start_pos, line_y, right_end_pos, line_y)
                    painter.drawLine(left_start_pos, line_y - 5, left_start_pos, line_y + 5)
                    painter.drawLine(right_end_pos, line_y - 5, right_end_pos, line_y + 5)

                    right_center = (right_start_pos + right_end_pos) // 2
                    arc_width = right_width
                    arc_rect = rect.adjusted(right_center - arc_width // 2, 55,
                                             -rect.width() + right_center + arc_width // 2, -80)
                    painter.drawArc(arc_rect, 0, 180 * 16)

            text_rect = rect.adjusted(0, 0, 0, 0)
            painter.drawText(text_rect, Qt.AlignCenter, self.display_text)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Program")
        self.setGeometry(100, 100, 600, 400)

        # Zmienne do przechowywania danych
        self.values_AB = {"A": "", "B": ""}
        self.values_CD = {"C": "", "D": "", "E": ""}

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # Górny rząd
        top_layout = QHBoxLayout()

        # Lewa kolumna (przyciski 1,2,3,4)
        left_layout = QVBoxLayout()

        # Przyciski 1 i 2
        self.button1 = QPushButton("1")
        self.button1.setFixedSize(120, 60)
        self.button1.clicked.connect(self.input_AB)

        self.button2 = QPushButton("2")
        self.button2.setFixedSize(120, 60)
        self.button2.clicked.connect(self.input_CD)

        left_layout.addWidget(self.button1)
        left_layout.addWidget(self.button2)

        # Przyciski 3 i 4 w jednym rzędzie
        bottom_buttons_layout = QHBoxLayout()
        self.button3 = QPushButton("3")
        self.button3.setFixedSize(80, 60)
        self.button3.clicked.connect(self.replace_C)

        self.button4 = QPushButton("4")
        self.button4.setFixedSize(80, 60)
        self.button4.clicked.connect(self.replace_D)

        bottom_buttons_layout.addWidget(self.button3)
        bottom_buttons_layout.addWidget(self.button4)
        left_layout.addLayout(bottom_buttons_layout)

        # Prawa kolumna (wyświetlacze 5 i 6)
        right_layout = QVBoxLayout()

        self.display5 = ArcDisplay("")
        self.display5.setFixedSize(300, 120)

        self.display6 = LineDisplay("")
        self.display6.setFixedSize(300, 120)

        right_layout.addWidget(self.display5)
        right_layout.addWidget(self.display6)

        top_layout.addLayout(left_layout)
        top_layout.addStretch()
        top_layout.addLayout(right_layout)

        # Dolny wyświetlacz (7)
        self.display7 = ComplexDisplay("")
        self.display7.setFixedHeight(120)

        main_layout.addLayout(top_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.display7)

        central_widget.setLayout(main_layout)

    def input_AB(self):
        dialog = InputDialog("Wprowadź wartości A i B", "A", "B", self)
        if dialog.exec_() == QDialog.Accepted:
            a, b = dialog.get_values()
            if a and b:
                self.values_AB["A"] = a
                self.values_AB["B"] = b
                self.display5.set_text(f"{a} ; {b}")

    def input_CD(self):
        dialog = InputDialog2("Wprowadź wartości C, D oraz e", "C", "D", "E", self)
        if dialog.exec_() == QDialog.Accepted:
            c, d, e = dialog.get_values()
            if c and d and e:
                self.values_CD["C"] = c
                self.values_CD["D"] = d
                self.values_CD["E"] = e
                self.display6.set_text(f"{c} ; {d} ; {e}")

    def replace_C(self):
        if self.values_AB["A"] and self.values_AB["B"] and self.values_CD["D"] and self.values_CD["E"]:
            a, b = self.values_AB["A"], self.values_AB["B"]
            d = self.values_CD["D"]
            e = self.values_CD["E"]
            result_text = f"{a} ; {b} ; {d}; {e}"
            self.display7.set_text(result_text, "arc_line")
        else:
            self.display7.set_text("Brak wymaganych danych")

    def replace_D(self):
        if self.values_AB["A"] and self.values_AB["B"] and self.values_CD["C"] and self.values_CD["E"]:
            a, b = self.values_AB["A"], self.values_AB["B"]
            c = self.values_CD["C"]
            e = self.values_CD["E"]
            result_text = f"{c} ; {a} ; {b}; {e}"
            self.display7.set_text(result_text, "line_arc")
        else:
            self.display7.set_text("Brak wymaganych danych")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()