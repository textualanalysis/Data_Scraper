def title(url):
    import requests 
    r = requests.get(url)
    from bs4 import BeautifulSoup  
    soup = BeautifulSoup(r.text, 'html.parser')  
    title = soup.find('h1', attrs={'class':'article-title'})
    if title  is not None:
        title=title.text.strip()
    else:
        print('[!] Request Failed')    
    return  title
    

def publish_date(url):
    import requests 
    r = requests.get(url)  
    from bs4 import BeautifulSoup  
    soup = BeautifulSoup(r.text, 'html.parser')  
    date = soup.find('div', attrs={'class':'published-date'})
    Posted_date=date.find('span', attrs={'class':'published-date__since'}).text.strip()
    if date  is not None:
        from dateutil.parser import parse
        month=parse(Posted_date).month
        day=parse(Posted_date).day
        year=parse(Posted_date).year
        date= str(month)+'/'+str(day)+'/'+str(year)
        
    else:
        print('[!] Request Failed')
    return date
    
def article(url):
    import requests 
    r = requests.get(url)
    from bs4 import BeautifulSoup  
    soup = BeautifulSoup(r.text, 'html.parser')  
    contents = soup.find_all('section', attrs={'class':'article-content'})
    article=""

    for content in contents :
        results = content.find_all('p')
        for result in results:
            article=article+ result.text.strip()
            
    else:
        print('[!] Request Failed')
    
    return article

def scraping(url):
    import requests 
    import pandas as pd
    r = requests.get(url)
    from bs4 import BeautifulSoup  
    soup = BeautifulSoup(r.text, 'html.parser')     
    record= []
    record.append((article(url),publish_date(url),title(url),url))
    
    df = pd.DataFrame(record, columns=['article', 'date', 'title', 'url'])   
    return df