import requests
from bs4 import BeautifulSoup
import re

def extract_stadium_info(country_id, stadium_name_filter):
    """Extraer información de los estadios de la web."""
    url = f'https://es.soccerwiki.org/country.php?action=stadiums&countryId={country_id}'
    stadium_data = []
    while url:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            stadiums = soup.find_all('a', href=lambda href: href and "/stadium.php?stadiumdid=" in href)
            
            for stadium in stadiums:
                stadium_url = f"https://es.soccerwiki.org{stadium['href']}"
                stadium_response = requests.get(stadium_url)
                if stadium_response.status_code == 200:
                    stadium_soup = BeautifulSoup(stadium_response.content, 'html.parser')
                    stadium_name_element = stadium_soup.find('h1', class_='h5 heading-component-title')
                    stadium_name = stadium_name_element.get_text(strip=True) if stadium_name_element else "Desconocido"
                    capacity_element = stadium_soup.find('p', class_='player-info-subtitle mb-2')
                    capacity_text = capacity_element.find('span', class_='text-dark', string=re.compile(r'Capacidad:'))
                    capacity = capacity_text.next_sibling.strip() if capacity_text else "Desconocido"
                    city_text = stadium_soup.find('span', class_='text-dark', string=re.compile(r'Ciudad:'))
                    city = city_text.next_sibling.strip() if city_text else "Desconocido"

                    if stadium_name != "Desconocido" and capacity != "Desconocido":
                        stadium_data.append({
                            'stadium': stadium_name,
                            'capacity': capacity,
                            'city': city
                        })
                        print(f"Stadium: {stadium_name}, Capacity: {capacity}, City: {city}")

            next_button = soup.find('a', class_='page-link', string=re.compile(r'Siguiente'))
            if next_button:
                next_page = next_button['href']
                url = f"https://es.soccerwiki.org{next_page}"
            else:
                url = None
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            break

    unique_stadium_data = {}
    for stadium in stadium_data:
        if stadium['stadium'] not in unique_stadium_data:
            unique_stadium_data[stadium['stadium']] = stadium

    stadium_data = list(unique_stadium_data.values())
    
    return stadium_data
