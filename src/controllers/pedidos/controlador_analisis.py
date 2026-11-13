from src.models.pedidos.modelo_analisis import AnalisisModel

class AnalisisController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.controller = self
        
        if hasattr(self.view, "after"):
            self.view.after(150, self.cargar_datos)
        else:
            self.cargar_datos()

    def cargar_datos(self, fecha_inicio=None, fecha_fin=None):
        if fecha_inicio is None and hasattr(self.view, "_fecha_inicio"):
            fecha_inicio = self.view._fecha_inicio
        if fecha_fin is None and hasattr(self.view, "_fecha_fin"):
            fecha_fin = self.view._fecha_fin

        data = self.model.get_dashboard_data(fecha_inicio, fecha_fin)
        self.view.actualizar_dashboard(data)
