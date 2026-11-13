import os
try:
    from openpyxl import Workbook
    from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

def guardar_como_excel(ruta_excel: str, filas: list, tipo="tabla") -> bool:
    if not HAS_OPENPYXL:
        raise ImportError("openpyxl no esta instalado. Instálalo usando: pip install openpyxl")
        
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte"
    
    # Escribir filas
    for fila in filas:
        ws.append(fila)
        
    # Estilos
    font_title = Font(name="Segoe UI", size=14, bold=True, color="333333")
    fill_title = PatternFill(start_color="EAEAEA", end_color="EAEAEA", fill_type="solid")
    
    font_header = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    fill_header = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    align_header = Alignment(horizontal="center", vertical="center")
    
    font_data = Font(name="Segoe UI", size=10)
    fill_zebra = PatternFill(start_color="F2F4F8", end_color="F2F4F8", fill_type="solid")
    align_data = Alignment(vertical="center", horizontal="left")
    
    borde_tenue = Side(border_style="thin", color="D9D9D9")
    borde_completo = Border(left=borde_tenue, right=borde_tenue, top=borde_tenue, bottom=borde_tenue)
    
    max_lengths = {}
    es_encabezado_siguiente = False
    data_row_counter = 0

    if tipo == "tabla":
        ws.freeze_panes = "A2"

    for row_idx, row in enumerate(ws.iter_rows(), start=1):
        # Ignorar filas totalmente vacias para estilos
        if not any(cell.value for cell in row):
            continue

        val = str(row[0].value) if row[0].value else ""
        
        # Logica para determinar el tipo de fila
        fila_tipo = "dato"
        
        if tipo == "tabla":
            if row_idx == 1:
                fila_tipo = "header"
            else:
                fila_tipo = "dato"
        else:
            # Multitabla
            if val.startswith("==="):
                fila_tipo = "titulo"
                es_encabezado_siguiente = True
                data_row_counter = 0
            elif es_encabezado_siguiente:
                fila_tipo = "header"
                es_encabezado_siguiente = False
            else:
                fila_tipo = "dato"
                data_row_counter += 1

        for col_idx, cell in enumerate(row, start=1):
            if cell.value is not None:
                cell.border = borde_completo
            
            if fila_tipo == "titulo":
                cell.font = font_title
                cell.fill = fill_title
                cell.alignment = Alignment(horizontal="left", vertical="center")
                cell.value = str(cell.value).replace("===", "").strip() if cell.value else ""
            elif fila_tipo == "header":
                cell.font = font_header
                cell.fill = fill_header
                cell.alignment = align_header
            else:
                cell.font = font_data
                cell.alignment = align_data
                if data_row_counter % 2 != 0 and tipo == "multitabla":
                    cell.fill = fill_zebra
                elif row_idx % 2 == 0 and tipo == "tabla":
                    cell.fill = fill_zebra
                    
            cell_len = len(str(cell.value)) if cell.value is not None else 0
            if col_idx not in max_lengths or cell_len > max_lengths[col_idx]:
                max_lengths[col_idx] = cell_len

        # Combinar celdas del titulo si es multitabla
        if fila_tipo == "titulo" and tipo == "multitabla":
            ws.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=2)

    # Ajuste automatico de columnas
    for col_idx, max_len in max_lengths.items():
        col_letter = get_column_letter(col_idx)
        adjusted_width = min(max_len + 5, 65)
        adjusted_width = max(adjusted_width, 12)
        ws.column_dimensions[col_letter].width = adjusted_width

    if tipo == "tabla":
        try:
            ws.auto_filter.ref = ws.dimensions
        except Exception:
            pass
            
    wb.save(ruta_excel)
    return True


def guardar_como_excel_analisis(ruta_excel: str, resumen: dict, top5: list, ventas_hora: list) -> bool:
    """
    Genera un Excel de Análisis de Productos con:
      - Hoja 'Reporte': tabla de resumen, top5 y ventas por hora (con AM/PM)
      - Gráfica de barras horizontal para Top 5 platos (con etiquetas de valor)
      - Gráfica de barras vertical para Ventas por hora (con etiquetas de valor)
    """
    if not HAS_OPENPYXL:
        raise ImportError("openpyxl no esta instalado. Instálalo usando: pip install openpyxl")

    from openpyxl.chart import BarChart, Reference
    from openpyxl.chart.series import SeriesLabel
    from openpyxl.chart.label import DataLabel, DataLabelList

    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte"

    # --- Estilos ---
    font_title   = Font(name="Segoe UI", size=15, bold=True, color="FFFFFF")
    fill_title   = PatternFill(start_color="8C1A11", end_color="8C1A11", fill_type="solid")
    font_header  = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    fill_header  = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    font_data    = Font(name="Segoe UI", size=10)
    fill_zebra   = PatternFill(start_color="F2F4F8", end_color="F2F4F8", fill_type="solid")
    align_center = Alignment(horizontal="center", vertical="center")
    align_left   = Alignment(horizontal="left",   vertical="center")
    borde_tenue  = Side(border_style="thin", color="D9D9D9")
    borde_completo = Border(left=borde_tenue, right=borde_tenue, top=borde_tenue, bottom=borde_tenue)

    def _apply(cell, font=None, fill=None, align=None, border=None):
        if font:   cell.font   = font
        if fill:   cell.fill   = fill
        if align:  cell.alignment = align
        if border: cell.border = border

    row = 1

    # === RESUMEN ===
    ws.cell(row=row, column=1, value="RESUMEN DE ANÁLISIS")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=2)
    _apply(ws.cell(row=row, column=1), font=font_title, fill=fill_title, align=align_center)
    row += 1

    for key, val in resumen.items():
        c1 = ws.cell(row=row, column=1, value=key)
        c2 = ws.cell(row=row, column=2, value=val)
        _apply(c1, font=Font(name="Segoe UI", size=10, bold=True), align=align_left, border=borde_completo)
        _apply(c2, font=font_data, align=align_left, border=borde_completo)
        if row % 2 == 0:
            c1.fill = fill_zebra; c2.fill = fill_zebra
        row += 1

    row += 1  # espacio

    # === TOP 5 ===
    top5_start_row = row
    ws.cell(row=row, column=1, value="TOP 5 PLATOS MÁS VENDIDOS")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=2)
    _apply(ws.cell(row=row, column=1), font=font_title, fill=fill_title, align=align_center)
    row += 1

    header_row_top5 = row
    for col, txt in enumerate(["Plato", "Total Vendido"], 1):
        c = ws.cell(row=row, column=col, value=txt)
        _apply(c, font=font_header, fill=fill_header, align=align_center, border=borde_completo)
    row += 1

    top5_data_start = row
    for i, item in enumerate(top5):
        c1 = ws.cell(row=row, column=1, value=str(item.get("nombre", "")))
        c2 = ws.cell(row=row, column=2, value=int(item.get("total_vendido", 0)))
        _apply(c1, font=font_data, align=align_left, border=borde_completo)
        _apply(c2, font=font_data, align=align_center, border=borde_completo)
        if i % 2 == 0:
            c1.fill = fill_zebra; c2.fill = fill_zebra
        row += 1
    top5_data_end = row - 1

    row += 1  # espacio

    # === VENTAS POR HORA ===
    hora_start_row = row
    ws.cell(row=row, column=1, value="VENTAS POR HORA")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=2)
    _apply(ws.cell(row=row, column=1), font=font_title, fill=fill_title, align=align_center)
    row += 1

    for col, txt in enumerate(["Hora del Día", "Cantidad de Pedidos"], 1):
        c = ws.cell(row=row, column=col, value=txt)
        _apply(c, font=font_header, fill=fill_header, align=align_center, border=borde_completo)
    row += 1

    hora_data_start = row
    for i, item in enumerate(ventas_hora):
        c1 = ws.cell(row=row, column=1, value=str(item.get("hora", "")))
        c2 = ws.cell(row=row, column=2, value=int(item.get("pedidos", 0)))
        _apply(c1, font=font_data, align=align_left, border=borde_completo)
        _apply(c2, font=font_data, align=align_center, border=borde_completo)
        if i % 2 == 0:
            c1.fill = fill_zebra; c2.fill = fill_zebra
        row += 1
    hora_data_end = row - 1

    # --- Ajuste de columnas ---
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 20

    # ============================================================
    # GRÁFICA 1: Top 5 Platos (barra horizontal) CON etiquetas
    # ============================================================
    if top5 and top5_data_end >= top5_data_start:
        chart_top5 = BarChart()
        chart_top5.type = "bar"          # horizontal
        chart_top5.grouping = "clustered"
        chart_top5.title = "Top 5 Platos Más Vendidos"
        chart_top5.y_axis.title = "Plato"
        chart_top5.x_axis.title = "Unidades Vendidas"
        chart_top5.style = 10
        chart_top5.width = 20
        chart_top5.height = 12

        data_ref = Reference(ws, min_col=2, min_row=header_row_top5, max_row=top5_data_end)
        cats_ref = Reference(ws, min_col=1, min_row=top5_data_start, max_row=top5_data_end)
        chart_top5.add_data(data_ref, titles_from_data=True)
        chart_top5.set_categories(cats_ref)
        chart_top5.series[0].graphicalProperties.solidFill = "8C1A11"

        # Etiquetas de datos: mostrar el valor al final de cada barra
        dLbls = DataLabelList()
        dLbls.showVal = True      # mostrar el número
        dLbls.showCatName = False # no repetir el nombre del eje
        dLbls.showSerName = False
        dLbls.showLegendKey = False
        dLbls.position = "outEnd"  # fuera del extremo de la barra
        chart_top5.series[0].dLbls = dLbls

        # Ocultar leyenda (el nombre del plato ya aparece en el eje Y)
        chart_top5.legend = None

        ws.add_chart(chart_top5, "D2")

    # ============================================================
    # GRÁFICA 2: Ventas por Hora (barra vertical) CON etiquetas
    # ============================================================
    if ventas_hora and hora_data_end >= hora_data_start:
        chart_hora = BarChart()
        chart_hora.type = "col"          # vertical
        chart_hora.grouping = "clustered"
        chart_hora.title = "Ventas por Hora del Día"
        chart_hora.x_axis.title = "Hora"
        chart_hora.y_axis.title = "Pedidos"
        chart_hora.style = 10
        chart_hora.width = 24
        chart_hora.height = 14

        data_ref = Reference(ws, min_col=2, min_row=hora_start_row + 1, max_row=hora_data_end)
        cats_ref = Reference(ws, min_col=1, min_row=hora_data_start, max_row=hora_data_end)
        chart_hora.add_data(data_ref, titles_from_data=True)
        chart_hora.set_categories(cats_ref)
        chart_hora.series[0].graphicalProperties.solidFill = "1F4E79"

        # Etiquetas de datos: mostrar el valor encima de cada barra
        dLbls_h = DataLabelList()
        dLbls_h.showVal = True       # mostrar el número de pedidos
        dLbls_h.showCatName = False  # no repetir la hora (ya aparece en el eje X)
        dLbls_h.showSerName = False
        dLbls_h.showLegendKey = False
        dLbls_h.position = "outEnd"  # encima de la barra
        chart_hora.series[0].dLbls = dLbls_h

        # Ocultar leyenda (la hora ya aparece en el eje X)
        chart_hora.legend = None

        # Rotar etiquetas del eje X para que las horas AM/PM quepan bien
        chart_hora.x_axis.tickLblSkip = 1
        chart_hora.x_axis.txPr = None  # dejar que Excel auto-rote

        # Anchor below the top5 chart (row ~22)
        ws.add_chart(chart_hora, "D22")

    wb.save(ruta_excel)
    return True
