APP_STYLE = """
QWidget {
    font-family: "JetBrains Mono", "Segoe UI", Arial, sans-serif;
    color: #A9B7C6;
    background: #2B2B2B;
}

QMainWindow {
    background: #2B2B2B;
}

QLabel#title {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 27px;
    font-weight: 700;
    color: #FFFFFF;
}

QLabel#subtitle {
    font-size: 13px;
    color: #808080;
}

QLabel#cardTitle {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #FFFFFF;
    min-height: 28px;
    max-height: 28px;
}

QLabel#componentName {
    min-width: 20px;
    max-width: 20px;
    padding-left: 3px;
    padding-right: 3px;
    qproperty-alignment: AlignCenter;
}

QFrame#preview {
    background: #5F96E6;
    border: 1px solid #555555;
    border-radius: 12px;
}

QLabel#hexPreview {
    font-family: "JetBrains Mono", Consolas, monospace;
    font-size: 15px;
    font-weight: 700;
    color: #FFFFFF;
}

QFrame#card {
    background: #313335;
    border: 1px solid #45494A;
    border-radius: 12px;
}

QLineEdit {
    background: #3C3F41;
    color: #A9B7C6;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 8px 10px;
    selection-background-color: #214283;
}

QLineEdit:focus {
    border: 1px solid #6897BB;
}

QComboBox {
    background: #3C3F41;
    color: #A9B7C6;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 5px 8px;
    min-width: 90px;
}

QComboBox:hover, QComboBox:focus {
    border: 1px solid #6897BB;
}

QComboBox QAbstractItemView {
    background: #3C3F41;
    color: #A9B7C6;
    selection-background-color: #214283;
}

QDoubleSpinBox {
    background: #3C3F41;
    color: #A9B7C6;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 3px 6px;
    min-height: 18px;
    selection-background-color: #214283;
}

QDoubleSpinBox:focus {
    border: 1px solid #6897BB;
}

QDoubleSpinBox::up-button,
QDoubleSpinBox::down-button {
    background: #3C3F41;
    border: none;
    width: 14px;
}

QSlider {
    min-height: 18px;
    max-height: 18px;
}

QSlider::groove:horizontal {
    height: 4px;
    background: #4B4D4F;
    border-radius: 2px;
}

QSlider::sub-page:horizontal {
    background: #6897BB;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    width: 12px;
    height: 12px;
    margin: -4px 0;
    border-radius: 6px;
    background: #6897BB;
}

QPushButton {
    background: #365880;
    color: #FFFFFF;
    border: 1px solid #4A6A8F;
    border-radius: 7px;
    padding: 8px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background: #41698F;
}

QPushButton#secondary {
    background: #3C3F41;
    border: 1px solid #555555;
    color: #A9B7C6;
}

QPushButton#secondary:hover {
    background: #45494A;
}

QPushButton#resetButton {
    background: #3C3F41;
    border: 1px solid #555555;
    color: #A9B7C6;
}

QPushButton#resetButton:hover {
    background: #45494A;
}
"""
