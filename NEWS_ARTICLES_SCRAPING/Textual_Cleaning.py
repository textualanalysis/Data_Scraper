def cleaning_textual(fname):
    #Importing libraries

    import re
    import string
    import nltk
    from textblob import Word
    from nltk.corpus import wordnet
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import TweetTokenizer 
    from nltk.corpus import stopwords
    import unicodedata
    from unidecode import unidecode
           
    # importing pandas package 
    import pandas as pd    
    df = pd.read_excel(fname+'.xlsx') 
    # Converting to lowercase
 
    df['tweet_clean_textual']= df['text'].str.lower()
    
    
    df['tweet_clean_textual']= df['tweet_clean_textual'].fillna("") 

    def deEmojify(inputString):
        return inputString.encode('ascii', 'ignore').decode('ascii')

        
    # Removing emoji
    df['tweet_clean_textual'] = df['tweet_clean_textual'].apply(lambda x: deEmojify(x))

    #Removing HTTP links
    df['tweet_clean_textual']= df['tweet_clean_textual'].str.replace(r"(https?\://)\S+", ' ')   
                             
    #Removing WWW links    
    df['tweet_clean_textual']= df['tweet_clean_textual'].str.replace(r'www.[A-Za-z0-9./?//:]\S+',' ') 

    # Removing hashtags
    df['tweet_clean_textual']= df['tweet_clean_textual'].str.replace(r'#[A-Za-z0-9]\S+', ' ')

    # Removing mentions  
    df['tweet_clean_textual']= df['tweet_clean_textual'].str.replace(r'@[A-Za-z0-9]\S+', ' ')

    #removing numbers
    df['tweet_clean_textual']= df['tweet_clean_textual'].str.replace(r'[0-9]+', ' ')

    #removing special character 
    df['tweet_clean_textual']= df['tweet_clean_textual'].str.replace(r'[^a-zA-Z0-9\s]+', ' ')

    #removing extra whitespaces
    df['tweet_clean_textual']= df['tweet_clean_textual'].str.strip()

    # Init Lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Get Part-of-speech (pos) tag of words of the sentence 
    def get_wordnet_pos(word):
        tag = nltk.pos_tag([word])[0][1][0].upper()

        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}

        return tag_dict.get(tag, wordnet.NOUN)

    # Lemmatize a Sentence with the appropriate Part-of-speech tag
    df['tweet_clean_textual'] = df['tweet_clean_textual'].apply(lambda x: " ".join([lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in x.split()]))

    #remove_stop_words using NLTK library
    stop = stopwords.words('english')

    df['tweet_clean_textual']=df['tweet_clean_textual'].apply(lambda x: " ".join([item for item in x.split() if item not in stop]))


    #Remove short words with less than 3 letters and remove_stop_words using  txt file
    def remove_short_stop_words(row):
        review = row['tweet_clean_textual']
        #Tokenize the sentence by using word_tokenize method from nltk library
        tokens = TweetTokenizer().tokenize(review)
        token_words = [w for w in tokens if len(w) >= 3]
        with open("additional_stop_words.txt",'r') as stopwordFile:
            #Tokenize the sentence by using split() method  from String library
            b=stopwordFile.read().split() 
            #remove_stop_words using txt file (additinal_stop_words)
            stop_words = [word for word in token_words if word not in b]
            joined_words = ( " ".join(stop_words))
        
            stopwordFile.close()

            return joined_words

    # Call the remove_short_words  function
    df['tweet_clean_textual'] = df.apply(remove_short_stop_words, axis=1)
    df.to_excel(filename+'.xlsx',encoding='utf-8',index=False) 

    # display 
    return df
