from api import api_fmcsa as api_fmc
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_data(usdot):
    api = api_fmc()
    cargo_carried = ''
    op_carried = ''
    
    try:
        data = api.search_cargo_carrier(usdot)
        for item in data:
            if item['cargoClassDesc'] is not None:
                cargo_carried += item['cargoClassDesc'] + ', '
        cargo_carried = cargo_carried.rstrip(', ')
    except Exception as e:
        print(f"Error fetching cargo carrier for USDOT {usdot}: {e}")
        
    try:
        data2 = api.operation_classification(usdot)
        for item in data2:
            if item['operationClassDesc'] is not None:
                op_carried += item['operationClassDesc'] + ', '
        op_carried = op_carried.rstrip(', ')
    except Exception as e:
        print(f"Error fetching operation classification for USDOT {usdot}: {e}")
        
    return cargo_carried, op_carried

if __name__ == '__main__':
    inicio_tiempo = time.time()
    
    data_list = pd.read_excel('cargue.xlsx')
    data_list['cargo_carrier'] = ''
    data_list['operation_classification'] = ''
    
    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers based on your system capability
        future_to_index = {executor.submit(fetch_data, round(int(row['USDOT']))): index for index, row in data_list.iterrows()}
        
        for future in as_completed(future_to_index):
            index = future_to_index[future]
            try:
                cargo_carried, op_carried = future.result()
                data_list.at[index, 'cargo_carrier'] = cargo_carried
                data_list.at[index, 'operation_classification'] = op_carried
                print('registro: ', index)
                print(cargo_carried)
            except Exception as exc:
                print(f'Error processing data for index {index}: {exc}')
    
    data_list.to_excel('fmcsalist.xlsx', index=False)
    
    fin_tiempo = time.time()
    tiempo_transcurrido = fin_tiempo - inicio_tiempo
    
    print('tiempo transcurrido: ', tiempo_transcurrido / 60)
