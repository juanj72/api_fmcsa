from api import api_fmcsa
from safer import search_phone
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_company(dot_number):
    """Función para procesar una compañía individualmente."""
    api = api_fmcsa()
    try:
        phone = search_phone(dot_number)
        results = api.search_dot(dot_number)
        results['phone_number'] = phone
        return results
    except Exception as e:
        print(f"Error con el DOT {dot_number}: {e}")
        return {'US DOT Number': dot_number, 'error': str(e)}

if __name__ == '__main__':
  
    data = pd.read_excel('dot_numbers.xlsx')

    first_data = data

    response = []

    with ThreadPoolExecutor(max_workers=5) as executor: 
      
        future_to_dot = {executor.submit(process_company, dot_number): dot_number for dot_number in first_data['DOT Numbers']}

        for future in as_completed(future_to_dot):
            dot_number = future_to_dot[future]
            try:
                result = future.result()
                print(f"Completado DOT {dot_number}")
                response.append(result)
            except Exception as e:
                print(f"Error procesando el DOT {dot_number}: {e}")
   
    dataframe = pd.DataFrame(response)

  
    dataframe.to_excel('authority_today.xlsx', index=False)
