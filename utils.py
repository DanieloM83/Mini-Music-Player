from PyQt6.QtCore import QFile, QTextStream


class StyleSheet(QFile):
    def __init__(self, stylesheet):
        path = "style/" + stylesheet
        super().__init__(path)

    def __enter__(self):
        self.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
        return QTextStream(self).readAll()

    def __exit__(self, *args):
        self.close()
