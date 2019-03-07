import urllib.request
from bs4 import BeautifulSoup
import os
import pymysql

origin = 'https://www.kanunu8.com'

url = 'https://www.kanunu8.com/book3/8196/'
#path = '白鹿原/'


db = pymysql.connect("localhost","root","zhgmen","zhgmen" )
cursor = db.cursor()




def parse_page(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    desc2 = soup.select('.p10-24')[1]
    for i in soup.select('tbody > tr > td > a'):
        print(i)
        
        if 'files' in i['href']:
            continue
        #if not os.path.exists(path):
            #os.makedirs(path)
        #data_file = os.path.join(path, i.string+'.txt')
        text = parse_content(url + i['href'])
        #save_file(data_file, text)
    
def parse_content(url):
    html = get_html(url)
    
    soup = BeautifulSoup(html, 'html.parser')
    return str(soup.select('td > p')[0])

    
def get_html(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    request = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(request)
    html = response.read().decode('gbk')
    
    return html

def save_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)

def get_author():
    html = get_html('https://www.kanunu8.com/author1.html')
    soup = BeautifulSoup(html, 'html.parser')
    l = soup.select('p > a')
    for item in l:
        if item.string == '努努书坊':
            break
        print(item)
        url = origin + item['href']
        html = get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        desc = str(soup.select('td>p')[0])
        #sql = "INSERT INTO authors(name,description) VALUES(%s,%s)"
        #cursor.execute(sql,(item.string, desc))
        print(soup.select('td > strong > a')[0]['href'])
        article = soup.select('td > strong > a')[0].string
        url = origin + soup.select('td > strong > a')[0]['href']
        #db.commit()
        print(url)
        html = get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        desc2 = soup.select('.p10-24')[1]
        print(desc2)
        sql = "INSERT INTO books(name,author,description) VALUES(%s,%s,%s)"
        cursor.execute(sql,(article,item.string, desc2))
        db.commit()

        for i in soup.select('tbody > tr > td > a'):
            print(i)
            break
        
            if 'files' in i['href']:
                continue
            #if not os.path.exists(path):
                #os.makedirs(path)
            #data_file = os.path.join(path, i.string+'.txt')
            text = parse_content(url + i['href'])
            #save_file(data_file, text)
        break
'''
desc 表名;
show columns from 表名;
describe 表名;
show create table 表名;
'''
        
def close_sql():
    pass
if __name__ == '__main__':
    get_author()
    cursor.close()
    db.close()
