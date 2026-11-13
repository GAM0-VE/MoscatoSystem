class AdminMesasController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)
        self.mesas_completas = []
        self.refresh_mesas()

    def refresh_mesas(self):
        self.mesas_completas = self.model.obtener_mesas()
        
        # Calculate stats
        total = len(self.mesas_completas)
        activas = sum(1 for m in self.mesas_completas if m['activo'])
        inactivas = total - activas
        self.view.update_stats(total, activas, inactivas)

        # Apply filters
        filtered = self.mesas_completas
        curr_filter = self.view.current_filter
        if curr_filter == "ACTIVAS":
            filtered = [m for m in filtered if m['activo']]
        elif curr_filter == "INACTIVAS":
            filtered = [m for m in filtered if not m['activo']]
            
        # Apply search
        search_q = self.view.get_search_query().lower()
        if search_q:
            filtered = [m for m in filtered if search_q in str(m['numero_mesa'])]
            
        self.view.render_table(filtered)

    def handle_add_mesa(self):
        self.view.open_mesa_form(None, None, self._save_mesa)

    def handle_edit_mesa(self, id_mesa, current_num):
        self.view.open_mesa_form(id_mesa, current_num, self._save_mesa)

    def _save_mesa(self, id_mesa, numero_mesa):
        if id_mesa is None:
            success, msg = self.model.agregar_mesa(numero_mesa)
        else:
            success, msg = self.model.editar_mesa(id_mesa, numero_mesa)
            
        if success:
            self.refresh_mesas()
        else:
            self.view.show_error(msg)

    def handle_toggle_mesa(self, id_mesa, activate):
        success, msg = self.model.cambiar_estado_activo(id_mesa, int(activate))
        if success:
            self.refresh_mesas()
        else:
            self.view.show_error(msg)
