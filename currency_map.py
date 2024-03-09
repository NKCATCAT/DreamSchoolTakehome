#%%
import requests
from bs4 import BeautifulSoup
def get_currency_map():
    requested_url = "https://www.11meigui.com/tools/currency"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.11meigui.com",
        "Sec-Ch-Ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    response = requests.get(requested_url,headers)
    page_source = BeautifulSoup(response.content, 'html.parser')
    centers = page_source.find_all('center')
    region_currency_symbols = {}

    for center in centers:
        region = center.get_text(strip=True)
        currency_symbols = {}  
        currency_table = center.find_next('table')

        for row in currency_table.find_all('tr')[2:]:  
            cols = row.find_all('td')  
            currency_name = cols[1].text.strip() 
            standard_symbol = cols[-2].text.strip()  
            currency_symbols[standard_symbol] = currency_name  
        region_currency_symbols[region] = currency_symbols
    return region_currency_symbols