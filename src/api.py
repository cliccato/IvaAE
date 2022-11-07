from re import findall
from requests import get
from bs4 import BeautifulSoup

def get_data(taxation, device_number):
    url = f"https://ivaservizi.agenziaentrate.gov.it/ser/mobile/fiscalizzazione/v1/stato/{taxation}?seed={device_number}"
    regex="[a-zA-Z0-9 ]+: "
    info=[]

    r = get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('ul', class_='file-info')
    datas = s.find_all('li')

    for x in range(0, 26):
        info.append(str(datas[x])[4:-5])
        result=findall(regex, info[x])
        if result:    info[x]=info[x].replace(result[0],"")
        info[x]=info[x].replace("\xa0","")
        info[x]=info[x].lstrip(' ')
                
    data = {
        "freshman": info[0],
        "state": info[1],
        "info": {
            "brand": info[3],
            "brand name": info[4],
            "model": info[5],
            "description": info[6],
            "seal type": info[7],
            "utilization": info[8]
        },
        "approval": {
            "number": info[10],
            "date": info[11]
        },
        "last verification": {
            "date": info[13],
            "outcome": info[14],
            "laboratory": info[15],
            "technician": info[16]
        },
        "last broadcast": info[18],
        "last update": {
            "date": info[20],
            "release": info[21],
            "release date": info[22]
        },
        "executive": {
            "vat": info[24],
            "name": info[25]
        }
    }

    return data
