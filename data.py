from openpyxl import load_workbook

def retorna_reservas(caminho_arquivo="RESERVAS.xlsx"):
    try:
        arquivo = load_workbook(caminho_arquivo, data_only=True)
        aba = arquivo['PLANILHA TRATADA']
        lista_reservas = []
        for professor, dia, motivo, sala  in aba.iter_rows(min_row=2,  max_col=4, values_only=True):
            reserva = {
            'professor': str(professor).strip(),
            'dia': str(dia).strip(),
            'motivo': str(motivo).strip(),
            'sala': str(sala).strip()
            }
            lista_reservas.append(reserva)
        return lista_reservas
    finally:
        arquivo.close()