import requests
from bs4 import BeautifulSoup
import json
import time

def get_champ_url():
    url = 'https://leagueoflegends.fandom.com/wiki/List_of_champions'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    champion_table = soup.find('table')  # Adjust if necessary

    championsUrl = []
    for row in champion_table.find_all('tr')[1:]:  # Skipping the header row
        columns = row.find_all('td')
        if len(columns) > 1:  # Ensure it's not an empty row
            # Step 4.1: Extract the champion name
            champion_link = columns[0].find('a')  # Find the first <a> tag that contains the link
            
            if champion_link:
                # Extract only the first part of the link to avoid URLs with "/LoL" or other suffixes
                champion_url = 'https://leagueoflegends.fandom.com' + champion_link['href']  
                champion_name = champion_link['title'].split('/LoL')[0]  # Extract the first word of the title
                
                img_tag = columns[0].find('img')
                if img_tag:
                    # Use 'data-src' for lazy-loaded images or 'src' for regular images
                    champion_icon = img_tag.get('data-src') or img_tag.get('src')
                else:
                    champion_icon = None

                championsUrl.append({'name': champion_name, 'url': champion_url, 'icon': champion_icon})

    return championsUrl


def get_champ_info(champ_url):

    NewChampion = {}
    NewChampion['name'] = champ_url['name']
    NewChampion['icon_url'] = champ_url['icon']
    NewChampion['positions'] = get_positions(champ_url)
    NewChampion['classes'] = get_champ_classes(champ_url)
    NewChampion['range'] = get_range(champ_url)
    NewChampion['adap_type'] = get_adap_type(champ_url)
    NewChampion['regions'] = get_champ_regions(champ_url)
    NewChampion['skins'] = get_skins(champ_url)

    return NewChampion


def get_range(champ_url):
    response = requests.get(champ_url['url'])
    soup = BeautifulSoup(response.text, 'html.parser')

    champ_range = ''

    range_section = soup.find('div', {'data-source': 'rangetype'})
    span_tags = range_section.find_all('span')
    for range_type in span_tags:
        champ_range = range_type.get_text(strip=True)
    
    return champ_range

def get_champ_classes(champ_url):
    response = requests.get(champ_url['url'])
    soup = BeautifulSoup(response.text, 'html.parser')

    champ_classes = []

    valid_classes = [ 'Fighter', 'Mage', 'Marksman', 'Assasin', 'Tank', 'Support']

    div_class = soup.find('div', {'data-source': 'legacy'} )

    span_tags = div_class.find_all('span')
    for champ_class in span_tags:
        champ_class = champ_class.get_text(strip=True)
        if champ_class in valid_classes:
            champ_classes.append(champ_class)

    return champ_classes

def get_positions(champ_url):
    response = requests.get(champ_url['url'])
    soup = BeautifulSoup(response.text, 'html.parser')

    champ_positions = []

    valid_roles = ['Top', 'Jungle', 'Middle', 'Bottom', 'Support']

    div_position = soup.find('div', {'data-source': 'position'})
    span_tags = div_position.find_all('span')
    for position in span_tags:
        position = position.get_text(strip=True)
        if position in valid_roles:
            champ_positions.append(position)

    return champ_positions


def get_adap_type(champ_url):
    response = requests.get(champ_url['url'])
    soup = BeautifulSoup(response.text, 'html.parser')

    champ_adap = ''

    adap_section = soup.find('div', {'data-source': 'adaptivetype'})
    a_tags = adap_section.find_all('a')
    for adap in a_tags:
        champ_adap = adap.get_text(strip=True)

    return champ_adap


def get_skins(champ_url):
    skin_url = champ_url['url'] + '/Cosmetics'
    response = requests.get(skin_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    champ_skins = []

    skins_section = soup.find_all('div', style='float:left')

    for skin in skins_section:
        skin_name = skin.get_text(strip=True).split('View in 3D')[0]
        champ_skins.append(skin_name)

    return champ_skins


def get_champ_regions(champ_url):
    
    response = requests.get(champ_url['url'].split('/LoL')[0])
    soup = BeautifulSoup(response.text, 'html.parser')

    valid_regions = ['Bandle City', 'Bilgewater', 'Camavor', 'Demacia', 'Freljord', 'Icathia', 'Ixtal', 'Ionia','Kathkan', 'Mount Targon', 'Noxus', 'Piltover', 'Runeterra', 'Shadow Isles', 'Shurima', 'The Void', 'Zaun'] 
    
    champ_regions= []

    # Find the specific section that contains the region information
    try :
        region_section = soup.find('div', {'data-source': 'region'})
        a_tags = region_section.find_all('a')
        for region in a_tags:
            region_text = region.get_text(strip=True)
            if region_text in valid_regions:
                champ_regions.append(region_text)
    except:
        champ_regions.append('Runeterra')
        
    return champ_regions


def fill_all_champ(champ_url):
    championsUrl = get_champ_url()
    all_champ_info = []

    for champ_url in championsUrl:
        champ_info = get_champ_info(champ_url)
        all_champ_info.append(champ_info)
        print(f"Champion {champ_url['name']} processed.")
        time.sleep(1)

    return all_champ_info

def save_champ_data(champ_data):
    with open('champions_lol.json', 'w') as json_file:
        json.dump(champ_data, json_file, indent=4)

    print("Champion data updated successfully.")



def main():
    all_champions = fill_all_champ(get_champ_url())
    save_champ_data(all_champions)


if __name__ == '__main__':
    main()