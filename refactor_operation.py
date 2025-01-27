from api import api_fmcsa as api_fmc
import pandas as pd
import time

if __name__ == '__main__':
    api = api_fmc()
    start_time = time.time()
    
    data = pd.read_excel('query.xlsx')
    if 'cargo_carrier' not in data.columns:
        data['cargo_carrier'] = None

    if 'operation_clasification' not in data.columns:
        data['operation_clasification'] = None

    for row in range(len(data)):

        print(f'registro {row} de {len(data)}')
        
        # Obtener datos del API
        cargo_carried_list = api.search_cargo_carrier(round(int(data['USDOT'][row])))
        operation_clasification = api.operation_classification(round(int(data['USDOT'][row])))

        # Procesar datos de cargo_carrier
        cargo_carrier = ', '.join(dat['cargoClassDesc'] for dat in cargo_carried_list)
        operation_list = ', '.join(dat['operationClassDesc'] for dat in operation_clasification)

        # Asignar valores fila por fila
        data.at[row, 'cargo_carrier'] = cargo_carrier
        data.at[row, 'operation_clasification'] = operation_list  # Aquí debe ser un valor para cada fila

    # Guardar el archivo actualizado
    data.to_excel('fmcsalist.xlsx', index=False)

    end_time = time.time()

    total_time = end_time-start_time
    print('tiempo transcurrido: ', total_time / 60)
