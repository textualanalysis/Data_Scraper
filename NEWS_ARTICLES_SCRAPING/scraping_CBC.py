
def title(url):
    
    import requests 
    r = requests.get(url)
    from bs4 import BeautifulSoup  
    soup = BeautifulSoup(r.text, 'html.parser')   
    title = soup.find('h1', attrs={'class':'detailHeadline'})
    if title  is not None:
        title=title.text.strip()
  
    return  title
    
def publish_date(url):
    import requests 
    r = requests.get(url)
    from bs4 import BeautifulSoup  
    soup = BeautifulSoup(r.text, 'html.parser')   

    date = soup.find('time', attrs={'class':'timeStamp'})
    
    if 'Posted' in date.string:
        Posted_date= date.string
        Posted_date = Posted_date.replace('Posted:', '')
        Posted_date=Posted_date[:Posted_date.find("|")]
        from dateutil.parser import parse
        month=parse(Posted_date).month
        day=parse(Posted_date).day
        year=parse(Posted_date).year
        publish_date= str(month)+'/'+str(day)+'/'+str(year)
     
                
    return publish_date
    
def article(url):
    import requests 
    r = requests.get(url)
    from bs4 import BeautifulSoup  
    soup = BeautifulSoup(r.text, 'html.parser')   
    
    content = soup.find('div', attrs={'class':'story'})
    article=""
    results = content.find_all('p')
    if results  is not None:
        for result in results:
            article=article+ result.text.strip()


    return article

def scraping(url):
    import requests 
    import pandas as pd
    from dateutil.parser import parse
    r = requests.get(url)
    from bs4 import BeautifulSoup  
    soup = BeautifulSoup(r.text, 'html.parser')     
    record= []
    record.append((article(url),publish_date(url),title(url),url))
    df = pd.DataFrame(record, columns=['article', 'date', 'title', 'url'])   
    return df