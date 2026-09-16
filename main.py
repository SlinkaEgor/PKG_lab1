import sys
from PyQt6.QtCore import Qt, QSignalBlocker
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication,
    QColorDialog,
    QDoubleSpinBox,
    QComboBox,
    QFrame,
    QSizePolicy,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from conversions import cmyk_to_all, hsv_to_all, rgb_to_all
from styles import APP_STYLE


class ComponentControl(QWidget):
    def __init__(self, name, minimum, maximum, decimals=1, callback=None):
        super().__init__()
        self.callback = callback
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Fixed
        )

        name_label = QLabel(name)
        name_label.setObjectName("componentName")

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(int(minimum * 10), int(maximum * 10))
        self.slider.setFixedHeight(18)

        self.spin = QDoubleSpinBox()
        self.spin.setRange(minimum, maximum)
        self.spin.setDecimals(decimals)
        self.spin.setSingleStep(1 if maximum <= 360 else 0.1)
        self.spin.setKeyboardTracking(False)
        self.spin.setFixedWidth(70)
        self.spin.setFixedHeight(28)

        top = QHBoxLayout()
        top.setContentsMargins(0, 0, 0, 0)
        top.setSpacing(8)
        top.addWidget(name_label)
        top.addStretch()
        top.addWidget(self.spin)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addLayout(top)
        layout.addWidget(self.slider)

        self.slider.valueChanged.connect(self._slider_changed)
        self.spin.valueChanged.connect(self._spin_changed)

    def _slider_changed(self, value):
        value = value / 10
        with QSignalBlocker(self.spin):
            self.spin.setValue(value)
        if self.callback:
            self.callback()

    def _spin_changed(self, value):
        with QSignalBlocker(self.slider):
            self.slider.setValue(round(value * 10))
        if self.callback:
            self.callback()

    def _format(self, value):
        return str(int(value)) if float(value).is_integer() else f"{value:.1f}"

    def set_gradient(self, colors):
        if not colors:
            return

        stops = []
        last = len(colors) - 1
        for index, color in enumerate(colors):
            position = index / last if last else 0
            stops.append(f"stop:{position:.3f} {color}")

        gradient = ", ".join(stops)
        self.slider.setStyleSheet(f"""
            QSlider {{
                min-height: 18px;
                max-height: 18px;
            }}
            QSlider::groove:horizontal {{
                height: 5px;
                border-radius: 2px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, {gradient});
            }}
            QSlider::sub-page:horizontal {{
                background: transparent;
            }}
            QSlider::add-page:horizontal {{
                background: transparent;
            }}
            QSlider::handle:horizontal {{
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
                background: #D7DCE2;
                border: 1px solid #7A8088;
            }}
        """)

    def set_value(self, value):
        with QSignalBlocker(self.spin), QSignalBlocker(self.slider):
            self.spin.setValue(value)
            self.slider.setValue(round(value * 10))
    def value(self):
        return self.spin.value()


class ModelCard(QFrame):
    def __init__(self, title, components, callback):
        super().__init__()
        self.setObjectName("card")
        self.controls = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        layout.addWidget(title_label)

        for name, minimum, maximum, decimals in components:
            control = ComponentControl(name, minimum, maximum, decimals, callback)
            self.controls.append(control)
            layout.addWidget(control)

    def set_gradients(self, gradients):
        for control, colors in zip(self.controls, gradients):
            control.set_gradient(colors)

    def values(self):
        return tuple(control.value() for control in self.controls)

    def set_values(self, values):
        for control, value in zip(self.controls, values):
            control.set_value(value)


class ColorConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Color Model Converter")
        self.resize(1100, 760)
        self.setMinimumSize(900, 650)
        self.updating = False

        root = QWidget()
        self.setCentralWidget(root)

        main_layout = QVBoxLayout(root)
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(18)

        header = QHBoxLayout()

        title_box = QVBoxLayout()
        title = QLabel("Color Model Converter")
        title.setObjectName("title")

        subtitle = QLabel("CMYK  ↔  RGB  ↔  HSV")
        subtitle.setObjectName("subtitle")

        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch()

        self.preview = QFrame()
        self.preview.setObjectName("preview")
        self.preview.setFixedSize(420, 210)

        preview_layout = QVBoxLayout(self.preview)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hex_preview = QLabel("#5F96E6")
        self.hex_preview.setObjectName("hexPreview")
        preview_layout.addWidget(self.hex_preview)

        header.addWidget(self.preview)
        main_layout.addLayout(header)

        color_row = QHBoxLayout()
        color_row.setSpacing(10)

        self.color_button = QPushButton("Выбрать цвет")
        self.color_button.setObjectName("secondary")
        self.color_button.clicked.connect(self.pick_color)

        self.hex_edit = QLineEdit("#5F96E6")
        self.hex_edit.setPlaceholderText("#RRGGBB")
        self.hex_edit.returnPressed.connect(self.from_hex)

        apply_button = QPushButton("Применить HEX")
        apply_button.clicked.connect(self.from_hex)

        color_row.addWidget(self.color_button)
        color_row.addWidget(self.hex_edit, 1)
        color_row.addWidget(apply_button)

        main_layout.addLayout(color_row)

        cmyk_options = QHBoxLayout()
        cmyk_options.setContentsMargins(0, 0, 0, 0)
        cmyk_label = QLabel("Алгоритм цветоделения:")
        self.cmyk_method = QComboBox()
        self.cmyk_method.addItems(["GCR", "UCR"])
        self.cmyk_method.currentTextChanged.connect(self.from_cmyk_method_changed)
        cmyk_options.addWidget(cmyk_label)
        cmyk_options.addWidget(self.cmyk_method)
        cmyk_options.addStretch()

        main_layout.addLayout(cmyk_options)

        cards = QHBoxLayout()
        cards.setSpacing(14)

        self.cmyk = ModelCard(
            "CMYK",
            [
                ("C", 0, 100, 1),
                ("M", 0, 100, 1),
                ("Y", 0, 100, 1),
                ("K", 0, 100, 1),
            ],
            self.from_cmyk,
        )

        self.rgb = ModelCard(
            "RGB",
            [
                ("R", 0, 255, 0),
                ("G", 0, 255, 0),
                ("B", 0, 255, 0),
            ],
            self.from_rgb,
        )

        self.hsv = ModelCard(
            "HSV",
            [
                ("H", 0, 360, 1),
                ("S", 0, 100, 1),
                ("V", 0, 100, 1),
            ],
            self.from_hsv,
        )

        cards.addWidget(self.cmyk)
        cards.addWidget(self.rgb)
        cards.addWidget(self.hsv)

        main_layout.addLayout(cards)

        reset_button = QPushButton("Сбросить")
        reset_button.setObjectName("resetButton")
        reset_button.setMinimumHeight(40)
        reset_button.clicked.connect(self.reset)

        main_layout.addWidget(reset_button)


        self.set_rgb(95, 150, 230)

    def update_preview(self, rgb):
        r, g, b = [round(max(0, min(255, value))) for value in rgb]
        hex_value = f"#{r:02X}{g:02X}{b:02X}"

        self.preview.setStyleSheet(
            f"QFrame#preview {{ background: rgb({r}, {g}, {b}); }}"
        )
        self.hex_preview.setText(hex_value)
        self.hex_edit.setText(hex_value)

        self.color_button.setStyleSheet(
            f"QPushButton {{ background: rgb({r}, {g}, {b}); color: white; "
            f"border: 1px solid #59657c; border-radius: 9px; padding: 8px 14px; }}"
        )

    def set_rgb(self, r, g, b):
        self.updating = True
        data = rgb_to_all(r, g, b, method=self.cmyk_method.currentText())

        self.rgb.set_values(data["RGB"])
        self.cmyk.set_values(data["CMYK"])
        self.hsv.set_values(data["HSV"])

        self.update_preview(data["RGB"])
        self.update_gradients()
        self.updating = False

    def from_rgb(self):
        if self.updating:
            return

        self.updating = True
        data = rgb_to_all(*self.rgb.values(), method=self.cmyk_method.currentText())

        self.cmyk.set_values(data["CMYK"])
        self.hsv.set_values(data["HSV"])

        self.update_preview(data["RGB"])
        self.update_gradients()
        self.updating = False

    def from_cmyk(self):
        if self.updating:
            return

        self.updating = True
        data = cmyk_to_all(*self.cmyk.values(), method=self.cmyk_method.currentText())

        self.rgb.set_values(data["RGB"])
        self.hsv.set_values(data["HSV"])

        self.update_preview(data["RGB"])
        self.update_gradients()
        self.updating = False

    def from_hsv(self):
        if self.updating:
            return

        self.updating = True
        data = hsv_to_all(*self.hsv.values())

        self.rgb.set_values(data["RGB"])
        self.cmyk.set_values(data["CMYK"])

        self.update_preview(data["RGB"])
        self.update_gradients()
        self.updating = False

    def from_cmyk_method_changed(self, _method):
        if self.updating:
            return
        self.from_rgb()

    def update_gradients(self):
        r, g, b = self.rgb.values()
        rgb_gradients = []
        for channel in range(3):
            colors = []
            for i in range(17):
                value = i * 255 / 16
                rgb = [r, g, b]
                rgb[channel] = value
                colors.append(QColor(round(rgb[0]), round(rgb[1]), round(rgb[2])).name())
            rgb_gradients.append(colors)
        self.rgb.set_gradients(rgb_gradients)

        c, m, y, k = self.cmyk.values()
        cmyk_gradients = []
        for channel in range(4):
            colors = []
            for i in range(17):
                value = i * 100 / 16
                values = [c, m, y, k]
                values[channel] = value
                rr, gg, bb = cmyk_to_all(*values, method=self.cmyk_method.currentText())["RGB"]
                colors.append(QColor(round(max(0, min(255, rr))), round(max(0, min(255, gg))), round(max(0, min(255, bb)))).name())
            cmyk_gradients.append(colors)
        self.cmyk.set_gradients(cmyk_gradients)

        h, ss, v = self.hsv.values()
        hsv_gradients = []
        for channel in range(3):
            colors = []
            for i in range(17):
                value = [i * 360 / 16, i * 100 / 16, i * 100 / 16][channel]
                values = [h, ss, v]
                values[channel] = value
                rr, gg, bb = hsv_to_all(*values)["RGB"]
                colors.append(QColor(round(max(0, min(255, rr))), round(max(0, min(255, gg))), round(max(0, min(255, bb)))).name())
            hsv_gradients.append(colors)
        self.hsv.set_gradients(hsv_gradients)

    def from_hex(self):
        text = self.hex_edit.text().strip()

        if not text.startswith("#"):
            text = "#" + text

        if len(text) != 7:
            return

        color = QColor(text)

        if not color.isValid():
            return

        self.set_rgb(color.red(), color.green(), color.blue())
        

    def pick_color(self):
        color = QColorDialog.getColor(
            QColor(self.hex_edit.text()),
            self,
            "Выберите цвет"
        )

        if color.isValid():
            self.set_rgb(color.red(), color.green(), color.blue())

    def reset(self):
        self.set_rgb(255, 255, 255)
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(APP_STYLE)

    window = ColorConverter()
    window.show()

    sys.exit(app.exec())
