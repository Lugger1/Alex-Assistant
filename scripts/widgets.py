from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtWidgets import QLabel, QWidget


class Label(QLabel):
    def __init__(self, parent:QWidget=None, text:str='QtLabel: <class="QLabel">', family='font/Exo2-VariableFont_wght.ttf', font_size=14) -> None:
        super().__init__()
        """
        Underclass for QLabel
        
        :param parent: parent for Label
        :param str text: string for Label
        :param str family: path for font family
        :param int font-size: font-size for text in Label   
        """
        
        self.setParent(parent)
        self.setText(text)
        # применение шрифта
        QFontDatabase.addApplicationFont(family)
        family_q = QFontDatabase.applicationFontFamilies(0)
        font = QFont(family_q, font_size)
        self.setFont(font)

