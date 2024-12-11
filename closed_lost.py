from api import api_fmcsa as api_fmc
import pandas as pd
import time


if __name__=='__main__':
    inicio_tiempo = time.time()
    api = api_fmc()
    data = pd.read_excel('closed_lost.xlsx')
    companies = []

    
    for index,row in data.iterrows():
        print(row['Deal Name'])
        mc = api.search_mc(api.get_dot(row['Associated Company']))
        phone = 'No apply'
        companies.append(api.search_name(row['Associated Company'],phone,mc['docketNumber'],row['Deal Name'],mc['prefix'],row['Record ID']))

    name_hb = pd.DataFrame(companies)
    name_hb.to_excel('closed_lost_result_final.xlsx',index=False)
    fin_tiempo = time.time()
    tiempo_transcurrido = fin_tiempo-inicio_tiempo
    print('tiempo transcurrido: ',tiempo_transcurrido/60,' minutos, registros: ', len(data))
