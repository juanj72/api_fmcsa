from api import api_fmcsa as api_fmc
import pandas as pd
import time

if __name__=='__main__':
    inicio_tiempo = time.time()
    api = api_fmc()
    data_list = pd.read_excel('init.xlsx')
    data_list['cargo_carrier'] = ''
    
    for index, row in data_list.iterrows():
        cargo_carried = '' # Reset cargo_carried for each row
        op_carried=''
        data = api.search_cargo_carrier(round(int(row['Usdot'])))
        data2 = api.operation_classification(round(int(row['Usdot'])))
        #print(data)
        
        for i in range(len(data)):
            # print(data[i]['cargoClassDesc'])
            if data[i]['cargoClassDesc'] is not None:
                cargo_carried += data[i]['cargoClassDesc'] + ', '
        data_list.at[index, 'cargo_carrier'] = cargo_carried.rstrip(', ')  # Assign value to DataFrame
        
        
        for i in range(len(data2)):
            # print(data[i]['cargoClassDesc'])
            if data[i]['operationClassDesc'] is not None:
                op_carried += data[i]['operationClassDesc'] + ', '
        data_list.at[index, 'operation_classification'] = op_carried.rstrip(', ')  # Assign value to DataFrame
        
        
        print('registro: ',index)

    data_list.to_excel('list_init.xlsx', index=False)

    fin_tiempo = time.time()
    tiempo_transcurrido = fin_tiempo - inicio_tiempo

    print('tiempo transcurrido: ', tiempo_transcurrido/60)
