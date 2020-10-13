def cleaning_sentiment(fname):
    #Importing libraries

    import re
    import string
    import emoji
    import nltk
    from textblob import Word
    from nltk.corpus import wordnet
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import TweetTokenizer
    
    
    # Happy Emoticons
    emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])
    # Sad Emoticons
    emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', ':3', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])
    
    # importing pandas package 
    import pandas as pd 
    
    df = pd.read_excel(fname+'.xlsx') 
    # Converting to lowercase
 
    df['tweet_clean_sentiment']= df['text'].str.lower()
    df['tweet_clean_sentiment']= df['tweet_clean_sentiment'].fillna("") 
    
    # Function for converting emoticons to sentiments (happy or sad)
    def convert_emoticons(row):
        text = row['tweet_clean_sentiment']
        tweet_tokenizer = TweetTokenizer()

        for word in tweet_tokenizer.tokenize(text):
           
            if word in emoticons_sad:         
                text = text.replace( word, ' sad ') 
                
            elif word in emoticons_happy:
                text = text.replace( word, ' happy ')
        return text
    
    # Convert emoticons to words {sad or happy}
    df['tweet_clean_sentiment'] = df.apply(convert_emoticons, axis=1)
    
    # Convert emoji to words
    df['tweet_clean_sentiment'] = df['tweet_clean_sentiment'].apply(lambda x: emoji.demojize(x))

    #replace apostrophe (’) by (') then apply the decontracted function 
    df['tweet_clean_sentiment']= df['tweet_clean_sentiment'].str.replace(r'\’', '\'')

    # Expending  contraction function
    def decontracted(row):
        sentence=row['tweet_clean_sentiment'] 
        # specific
        sentence = re.sub(r"won\'t", "will not", sentence)       
        sentence = re.sub(r"can\'t", "cannot", sentence)
        sentence = re.sub(r"shan\'t", "shall not", sentence)
        sentence = re.sub(r"wanna", "want to", sentence) 
        sentence = re.sub(r"let's", "let us", sentence)
        sentence = re.sub(r"innit", "is it not", sentence)
        sentence = re.sub(r"gonna", "going to", sentence)
        sentence = re.sub(r"gotta", "got to", sentence)

        # general
        sentence = re.sub(r"n\'t", " not", sentence)
        sentence = re.sub(r"\'re", " are", sentence)
        sentence = re.sub(r"\'s", " is", sentence)
        sentence = re.sub(r"\'d", " would", sentence)   
        #sentence = re.sub(r"\'d", " had", sentence)    
        sentence = re.sub(r"\'ll", " will", sentence)
        #sentence = re.sub(r"\'ll", " shall", sentence)
        sentence = re.sub(r"\'t", " not", sentence)
        sentence = re.sub(r"\'ve", " have", sentence)
        sentence = re.sub(r"\'m", " am", sentence)
        
        return sentence
    # Expending  contraction
    df['tweet_clean_sentiment'] = df.apply(decontracted, axis=1)
    
    #Removing HTTP links
    df['tweet_clean_sentiment']= df['tweet_clean_sentiment'].str.replace(r"(https?\://)\S+", ' ')   
                             
    #Removing WWW links    
    df['tweet_clean_sentiment']= df['tweet_clean_sentiment'].str.replace(r'www.[A-Za-z0-9./?//:]\S+',' ') 

    # Removing hashtags
    df['tweet_clean_sentiment']= df['tweet_clean_sentiment'].str.replace(r'#[A-Za-z0-9]\S+', ' ')

    # Removing mentions  
    df['tweet_clean_sentiment']= df['tweet_clean_sentiment'].str.replace(r'@[A-Za-z0-9]\S+', ' ')

    #removing numbers
    df['tweet_clean_sentiment']= df['tweet_clean_sentiment'].str.replace(r'[0-9]+', ' ')

    #removing special character 
    df['tweet_clean_sentiment']= df['tweet_clean_sentiment'].str.replace(r'[^a-zA-Z0-9-\s]+', ' ')

    #removing extra whitespaces
    df['tweet_clean_sentiment']= df['tweet_clean_sentiment'].str.strip()

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
    df['tweet_clean_sentiment'] = df['tweet_clean_sentiment'].apply(lambda x: " ".join([lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in x.split()]))

    # Connect with NO 
    df['tweet_clean_sentiment']= df['tweet_clean_sentiment'].str.replace(r'no ', 'no_')

    # Connect with NOT 
    df['tweet_clean_sentiment']= df['tweet_clean_sentiment'].str.replace(r'not ', 'not_')


    #Remove stop_words using stop txt file
    def remove_stop_words(row):
        with open("stop.txt",'r') as stopwordFile:
            #Tokenize the sentence by using split() method  from String library
            b=stopwordFile.read().split() 
            review = row['tweet_clean_sentiment']
            tokens = TweetTokenizer().tokenize(review)
            stop_words = [word for word in tokens if word not in b]
            remove_words = ( " ".join(stop_words))
            stopwordFile.close()
            return remove_words
        
        # Call the remove_stop_words function   
    df['tweet_clean_sentiment'] = df.apply(remove_stop_words, axis=1)

    #Remove short words with less than 3 letters
    def remove_short_words(row):
        review = row['tweet_clean_sentiment']
        #Tokenize the sentence by using word_tokenize method from nltk library
        tokens = TweetTokenizer().tokenize(review)
        token_words = [w for w in tokens if len(w) >= 3]
        joined_words = ( " ".join(token_words))
        return joined_words

    # Call the remove_short_words function
    df['tweet_clean_sentiment'] = df.apply(remove_short_words, axis=1)
  
    # Replace hyphen "-" with underscore "_". 
    df['tweet_clean_sentiment']= df['tweet_clean_sentiment'].str.replace(r'-', '_')
    df.to_excel(filename+'TextualSentimentclean.xlsx',encoding='utf-8',index=False) 
   
    return df
