def title(url):
    import requests 
    import pandas as pd
    r = requests.get(url)
    from bs4 import BeautifulSoup  
    soup = BeautifulSoup(r.text, 'html.parser')  
    title = soup.find('h1', attrs={'class':'l-article__title'}).text.strip()
    return  title
    
def publish_date(url):
    from datetime import datetime
    import requests 
    import re
    import pandas as pd
    r = requests.get(url)
    from bs4 import BeautifulSoup  
    soup = BeautifulSoup(r.text, 'html.parser')  
    date = soup.find('div', attrs={'id':'bylineDateUpdated'}).text.strip()
    date=date.replace('Updated', '')
    date=date.replace(',', '')
    from dateutil.parser import parse
    month=parse(date).month
    day=parse(date).day
    year=parse(date).year
    date= str(month)+'/'+str(day)+'/'+str(year)
   
    return date    
    
def article(url):
    import requests 
    import pandas as pd
    r = requests.get(url)
    from bs4 import BeautifulSoup  
    soup = BeautifulSoup(r.text, 'html.parser')  
    blacklist = ['div','a']
    article=""
    results = soup.find_all('p')
    for result in results:
        if result.parent.name not in blacklist: 
            article=article+ result.text.strip()

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