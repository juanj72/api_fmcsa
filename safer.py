import requests
from bs4 import BeautifulSoup

def search_phone(dot):
    # URL del sitio web que deseas scrappear
    url = f'https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string={dot}'

    # Realiza la solicitud HTTP
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers, timeout=30)

    # Verifica si hubo algún error en la solicitud
    if response.status_code != 200:
        print(f'Error al hacer la solicitud: {response.status_code}')
        return

    # Procesa la respuesta
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encuentra todos los elementos "tr"
    rows = soup.find_all('tr')

    # Busca la fila que contiene "Phone:"
    for row in rows:
        th = row.find('th')
        if th and th.text.strip() == 'Phone:':
            td = row.find('td')
            if td:
                return td.text.strip()

    return None

# Ejemplo de uso
# dot_number = '4251141'  # Reemplaza con el número USDOT que deseas buscar
# phone = search_phone(dot_number)
# if phone:
#     print(f'Phone: {phone}')
# else:
#     print('No se encontró el número de teléfono.')
