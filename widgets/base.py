from PyQt6.QtWidgets import QWidget


class BaseWidget(QWidget):
    def resize_widget(self, per_x: float, per_y: float, per_w: float, per_h: float, parent=None, centered=False):
        par_geom = self.parent().geometry() if parent is None else parent.geometry()
        par_x, par_y, par_w, par_h = par_geom.x(), par_geom.y(), par_geom.width(), par_geom.height()
        if centered:
            w, h = int(par_w * per_w), int(par_h * per_h)
            x, y = int(par_w * per_x - w // 2), int(par_h * per_y - h // 2)
            self.setGeometry(x, y, w, h)
            return {"x": x, "y": y, "w": w, "h": h}
        x, y, w, h = int(par_w * per_x), int(par_h * per_y), int(par_w * per_w), int(par_h * per_h)
        self.setGeometry(x, y, w, h)
        return {"x": x, "y": y, "w": w, "h": h}

    def calculate(self, per_x: float, per_y: float, per_w: float, per_h: float, parent=None, centered=False) -> dict:
        par_geom = self.parent().geometry() if parent is None else parent.geometry()
        par_x, par_y, par_w, par_h = par_geom.x(), par_geom.y(), par_geom.width(), par_geom.height()
        if centered:
            w, h = int(par_w * per_w), int(par_h * per_h)
            x, y = int(par_w * per_x - w // 2), int(par_h * per_y - h // 2)
            return {"x": x, "y": y, "w": w, "h": h}
        x, y, w, h = int(par_w * per_x), int(par_h * per_y), int(par_w * per_w), int(par_h * per_h)
        return {"x": x, "y": y, "w": w, "h": h}
