def title(url):
    import requests 
    r = requests.get(url)
    from bs4 import BeautifulSoup  
    soup = BeautifulSoup(r.text, 'html.parser')  
    title = soup.find('h1', attrs={'class':'page-title'})
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
    date = soup.find('time', attrs={'class':'datetime'})
    if date  is not None:
        from dateutil.parser import parse
        month=parse(date.string).month
        day=parse(date.string).day
        year=parse(date.string).year
        date= str(month)+'/'+str(day)+'/'+str(year)
    else:
        print('[!] Request Failed')
    return date
    
def article(url):
    import requests 
    r = requests.get(url)
    from bs4 import BeautifulSoup  
    soup = BeautifulSoup(r.text, 'html.parser')  
    content = soup.find('div', attrs={'class':'article-content'})
    article=""
    blacklist = ['footer','details','a']
    results = content.find_all('p')
    if results  is not None:
        for result in results:
            if result.parent.name not in blacklist: 
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