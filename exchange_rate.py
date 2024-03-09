import requests
from bs4 import BeautifulSoup
import argparse
from currency_map import get_currency_map  #获取货币名词与标准符号对应关系
from datetime import datetime
def get_exchange_request(requested_url, currency_name,date):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Length": "45",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "srh.bankofchina.com",
        "Origin": "https://www.boc.cn",
        "Referer": "https://www.boc.cn/",
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

    data = {
    'erectDate': '',  
    'nothing': date,
    'pjname': currency_name, 
    'head': 'head_620.js',  
    'bottom': 'bottom_591.js',  
    }

    response = requests.post(requested_url, headers=headers, data=data)
    return response
def parse_data(response):
    page_source = BeautifulSoup(response.content, 'html.parser')
    table = page_source.find('div', class_='BOC_main publish').find('table')
    rows = table.find_all('tr')
    if len(rows) == 0:
        print("Cannot find the match currency name")
    columns = rows[1].find_all('td') 
    exchange_sell_price = columns[3].text.strip()  
    return exchange_sell_price
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='keywords')
    parser.add_argument('date', type=str, help='format YYYY-MM-DD')
    parser.add_argument('currency_symbol', type=str, help='currency symbol')
    args = parser.parse_args()
    if datetime.strptime(args.date, "%Y-%m-%d") >= datetime.now():
        print("Cannot fetch future data")
        exit(1)
    currency_map = get_currency_map()
    for region in currency_map:
        currency_name = currency_map[region].get(args.currency_symbol.upper())
        if currency_name:
            break
    if not currency_name:
        print(f"Currency symbol {args.currency_symbol} not found.")
        exit(1)
    requested_url = "https://srh.bankofchina.com/search/whpj/search_cn.jsp"
    response = get_exchange_request(requested_url, currency_name, args.date)

    if response.status_code == 200:
        exchange_price = parse_data(response)
        print(exchange_price)
        with open('result.txt', 'w') as file:
            file.write(f"{args.date} {args.currency_symbol} {exchange_price}\n")
    else:
        print("Failed to retrieve data.")