from api import api_fmcsa as api_fmc
import pandas as pd
import time


if __name__=='__main__':
    inicio_tiempo = time.time()
    api = api_fmc()
    data = pd.read_excel('NoPhone.xlsx')
    companies = []

    
    for index,row in data.iterrows():
        print(row['Company name'])
        mc = api.search_mc(api.get_dot(row['Company name']))
        if row['Phone Number']=='':
            phone = 11111
        else:
            phone = row['Phone Number']
        companies.append(api.search_name(row['Company name'],phone,mc['docketNumber'],row['Company name'],mc['prefix'],row['Record ID']))

    name_hb = pd.DataFrame(companies)
    name_hb.to_excel('namhb.xlsx',index=False)
    fin_tiempo = time.time()
    tiempo_transcurrido = fin_tiempo-inicio_tiempo
    print('tiempo transcurrido: ',tiempo_transcurrido/60,' minutos, registros: ', len(data))

