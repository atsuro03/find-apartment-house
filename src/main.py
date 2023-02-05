from bs4 import BeautifulSoup
from lineNotifyBot import LINENotifyBot
from itemData import ItemData
import requests

def scrape():
    base_url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&pc=50&smk=&po1=25&po2=99&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&sc=13106&sc=13107&sc=13108&sc=13118&sc=13121&sc=13122&sc=13123&sc=13109&sc=13110&sc=13111&sc=13112&sc=13114&sc=13115&sc=13120&sc=13116&sc=13117&sc=13119&ta=13&cb=0.0&ct=7.0&md=02&md=03&md=05&ts=1&ts=2&et=15&mb=0&mt=9999999&cn=30&tc=0400301&tc=0400501&tc=0400601&fw2=&{}'
    max_page = 5
    page_data_list = {}

    for page in range(1, max_page + 1):
        url = base_url.format('page=' + str(page))
        soup = getHtml(url)
        items = soup.find_all('div', {'class': 'cassetteitem'})
        
        for item in items:
            category        = item.find('div', {'class': 'cassetteitem_content-label'}).text.strip()
            house_name      = item.find('div', {'class': 'cassetteitem_content-title'}).text.strip()
            address         = item.find('li', {'class': 'cassetteitem_detail-col1'}).text.strip()
            access          = item.find('li', {'class': 'cassetteitem_detail-col2'}).text.strip()
            year_built      = item.find('li', {'class': 'cassetteitem_detail-col3'}).find_all('div')[0].text.strip()
            structure       = item.find('li', {'class': 'cassetteitem_detail-col3'}).find_all('div')[1].text.strip()
            floor           = item.find_all('td')[2].text.strip()
            rent            = item.find_all('td')[3].find_all('li')[0].text.strip()
            admin_expenses  = item.find_all('td')[3].find_all('li')[1].text.strip()
            deposit         = item.find_all('td')[4].find_all('li')[0].text.strip()
            reward          = item.find_all('td')[4].find_all('li')[1].text.strip()
            layout          = item.find_all('td')[5].find_all('li')[0].text.strip()
            capacity        = item.find_all('td')[5].find_all('li')[1].text.strip()

            item_info = ItemData(
                category,
                house_name,
                address,
                access,
                year_built,
                structure,
                floor,
                rent,
                admin_expenses,
                deposit,
                reward,
                layout,
                capacity
            )

            property_info = {
                'item_info': item_info
            }

            page_data_list[page] = property_info

    return page_data_list
 
def getHtml(url):
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.content, 'html.parser')
    return soup

def createMessage():
    message = ''
    scrape_data_list = scrape()

    for i in range(1, len(scrape_data_list)+1):
        message += str(i) + 'ページ\n'
        message += 'カテゴリ： ' + scrape_data_list[i]['item_info'].category + '\n'
        message += '名称： ' + scrape_data_list[i]['item_info'].house_name + '\n'
        message += '住所： ' + scrape_data_list[i]['item_info'].address + '\n'
        message += 'アクセス： ' + scrape_data_list[i]['item_info'].access + '\n'
        message += '築年数 ' + scrape_data_list[i]['item_info'].year_built + '\n'
        message += '構造： ' + scrape_data_list[i]['item_info'].structure + '\n'
        message += '階： ' + scrape_data_list[i]['item_info'].floor + '\n'
        message += '賃料： ' + scrape_data_list[i]['item_info'].rent + '\n'
        message += '管理費： ' + scrape_data_list[i]['item_info'].admin_expenses + '\n'
        message += '敷金： ' + scrape_data_list[i]['item_info'].deposit + '\n'
        message += '礼金： ' + scrape_data_list[i]['item_info'].reward + '\n'
        message += '間取り： ' + scrape_data_list[i]['item_info'].layout + '\n'
        message += '専有面積： ' + scrape_data_list[i]['item_info'].capacity + '\n'
        
        if i != len(scrape_data_list):
            message += '\n'

    return message

def main():
    bot = LINENotifyBot(access_token='YOUR_ACCESS_TOKEN')
    bot.send(message=createMessage())

if __name__ == '__main__':
    main()