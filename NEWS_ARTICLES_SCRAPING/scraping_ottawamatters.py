def title (url):
    import requests 
    r = requests.get(url)
    from bs4 import BeautifulSoup  
    soup = BeautifulSoup(r.text, 'html.parser')   
    
    title = soup.find('h1', attrs={'class':'title details-title'})
  
    if title  is not None:
        title=title.text.strip()
    else:
        print('[!] Request Failed')    
    return  title
    

    
def publish_date(url):
    from datetime import datetime
    import requests 
    r = requests.get(url)
    from bs4 import BeautifulSoup  
    soup = BeautifulSoup(r.text, 'html.parser')   

    date = soup.find('div', attrs={'class':'col-md-7 details-byline'})
    Posted_date=date.find('time', attrs={'class':'timeago'}).text.strip()
   
    from dateutil.parser import parse
    month=parse(Posted_date).month
    day=parse(Posted_date).day
    year=parse(Posted_date).year
    date= str(month)+'/'+str(day)+'/'+str(year)
                
    return date


def article(url):
    import requests 
    r = requests.get(url)
    from bs4 import BeautifulSoup  
    soup = BeautifulSoup(r.text, 'html.parser')   
    
    content = soup.find('div', attrs={'id':'details-body'})
    article=""
   
    results = content.find_all('p')
    
    if results  is not None:
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

    return article
