import urllib.request
from bs4 import BeautifulSoup
import os
import pymysql
import re

origin = 'https://www.kanunu8.com'

url = 'https://www.kanunu8.com/book3/8196/'



db = pymysql.connect("localhost","root","zhgmen","zhgmen" )
cursor = db.cursor()





    
def parse_content(url):
    html = get_html(url)
    
    soup = BeautifulSoup(html, 'html.parser')
    return str(soup.select('td > p')[0])

    
def get_html(url):
    header = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    request = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(request)
    html = response.read().decode('gbk')
    
    return html

def save_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)

def get_author():#爬取作者以及图书，建立数据库
    html = get_html('https://www.kanunu8.com/author2.html')
    soup = BeautifulSoup(html, 'html.parser')
    l = soup.select('p > a')
    for item in l:#遍历作者
        if item.string == '努努书坊':
            break
        
        author_name = item.string
        url = origin + item['href']
        html = get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        desc = str(soup.select('td>p')[0])
        
        sql = "INSERT INTO authors(name,description) VALUES(%s,%s)"
        cursor.execute(sql,(author_name, desc))
        db.commit()
#存入数据表auhors字段作者和描述

        
        #articles = soup.select('td > strong > a')
        
        articles = soup.select('.p10-24')[:-2]
        
        for article in articles:#遍历作品
            link = origin + article.strong.a['href']
            book_name = article.strong.a.string
            desc2 = article.br.next_sibling.string
            if link[-5:] == '.html': #短片小说 独立的表short
                text = parse_content(link)
                sql = "INSERT INTO short(name, author, content) VALUES(%s,%s,%s)"
        
                cursor.execute(sql,(book_name, author_name, text))
                db.commit()
                continue
            #print(link,author_name,book_name,desc2)
            
            sql = "INSERT INTO books(name, author, link, description) VALUES(%s,%s,%s,%s)"
        
            cursor.execute(sql,(book_name, author_name, link, desc2))
            db.commit()
#存入数据表books字段 
        


        
'''
desc 表名;
show columns from 表名;
describe 表名;
show create table 表名;
'''

        #save_file(data_file, text)

    
def get_link():#查询书本连接创建小说数据库，导入内容
    sql = "SELECT name,author,link FROM books"
    cursor.execute(sql)
    results = cursor.fetchall()
    
    for row in results:
        
        book_name = row[0]
        author = row[1]
        link = row[2]
        re_ = re.match( r'《(.*?)》', book_name)
        if re_:
            table_name = re_.group(1)
        else:
            
            
            continue
        
        

        print(book_name,author,link)
        sql = 'create table {}(id int(4) not null PRIMARY KEY auto_increment,chapter varchar(10),content LONGTEXT not null)'.format(table_name)
        cursor.execute(sql)
        html = get_html(link)
        
        soup = BeautifulSoup(html, 'html.parser')
       
        for i in soup.select('tbody > tr > td > a'):
        
        
            if 'files' in i['href']:
                continue
            links = link + i['href']
            print(link)
            chapter = i.string
           
        
            text = parse_content(links)
            print(chapter,text)
            sql = "INSERT INTO {}(chapter, content) VALUES(%s,%s)".format(table_name)
            cursor.execute(sql,(chapter,text))
            db.commit()

        

       


        
def close_sql():
    cursor.close()
    db.close()
if __name__ == '__main__':
    #get_author()
    get_author()
    get_link()
    close_sql()
