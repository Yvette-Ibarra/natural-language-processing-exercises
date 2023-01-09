
from bs4 import BeautifulSoup
import re
import pandas as pd

import requests

######################## code up ############################

def basic_info(url):
    '''
    basic infor takes in a url from codeupblog and retrieves infromation from website:
    title, publish_date, content and returns a dictionary with information
    '''
    blog_info={"title","publish_date","content"}
    headers = {'User-Agent': 'Codeup Data Science'}
    response = requests.get(url, headers=headers)
    
    #find the title
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1')
    
    
    #Access the date published
    publish_date = soup.find('span', class_='published')
 
    
    #Access the article content
    content = soup.find('div', class_='entry-content')

    output = {
        'title': title.text,
        'publish_date': publish_date.text,
        'content': content.text
     }
    return output

def codeup_blog():
    '''
    codeup_blog has not input
    request access to codeup blog saves links from articles and runs a loop through 
    codeup blog articles to retrieve information: title and content.

    returns articles infromation from code up in a dictionary form
    '''
    url = 'https://codeup.com/blog/'
    headers = {'User-Agent': 'Codeup Data Science'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    links = [link['href'] for link in soup.select('.more-link')]

    articles = []

    for url in links:

        url_response = requests.get(url, headers=headers)
        soup = BeautifulSoup(url_response.text)

        title = soup.find('h1', class_='entry-title').text
        content = soup.find('div', class_='entry-content').text.strip()

        article_dict = {
            'title': title,
            'content': content
        }

        articles.append(article_dict)
        return articles

######################## inshorts ########################################

def get_info(url):

    '''
    get_info rquest acess to inshorts website   and retrieves information of one article
    on page: 'title','date','author','content','source_link'
    returns information in a dataframe
    '''
    output =[]
    response = requests.get(url)
    response = response.content 
    soup = BeautifulSoup(response,'html.parser')
    
    # main branch
    card_stack = soup.find('div',class_ ='card-stack')
    # article branch
    article_info = card_stack.find('div', class_ ='news-card z-depth-1')
     
    # get title
    a_ = article_info.find('a')
    #headline = a_.find_all('span', attr)
    title = a_.find(itemprop ='headline').get_text()
    
    # get published date
    date = article_info.find('span', class_= 'date').text
    
    # get author
    author = article_info.find('span', class_= 'author').text
    
    # get content
    content = article_info.find('div', itemprop='articleBody').text
    
    # get source link
    source = article_info.find('a', class_= 'source')
    pattern = re.compile(r'(www.*?)\s')
    link = pattern.findall(str(source))
    link = link[0]
    
    output.append([title,date,author,content,link])
    
    output_df = pd.DataFrame(output, columns = ['title','date','author','content','source_link'])
    return output_df

def inshort_info():
    '''
    inshort_info has no input:
    funciton request access to website and retrieves information of websites articles:
    title, content, category
    returns a list of information from articles
    '''
    url='https://www.inshorts.com/en/read'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    
    # put it together
    categories = [li.text.lower() for li in soup.select('li')[1:]]
    categories[0]='national'

    inshorts = []
    for cat in categories:
        url = 'https://www.inshorts.com/en/read' + '/'+ cat
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        titles = [span.text for span in soup.find_all('span', itemprop = 'headline')]
        contents = [div.text for div in soup.find_all('div', itemprop = 'articleBody')]
    
        for i in range(len(titles)):

            article = {

                'title': titles[i],
                'content': contents [i],
                'category': cat
            }

            inshorts.append(article)
    return inshorts