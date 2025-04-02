from urlextract import URLExtract
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import emoji
extractor = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user !="overall":
         # If a specific user is selected, filter the dataframe and get the number of messages for that user

        df = df[df['user'] == selected_user]
    
    num_messages = df.shape[0]  # number of messages for the selected user

    words = []
    for message in df['message']:
        words.extend(message.split())

    ## fetch number of media messages

    no_of_media_messages = df[df['message'] == '<Media omitted>'].shape[0]
    
    ## fetch number of URLs
    links = []

    for message in df['message']:
        links.extend(extractor.find_urls(message))


        
    return num_messages, len(words), no_of_media_messages, len(links)

        
def most_busy_users(df):
    # Get the top 5 users with the highest number of messages
    x = df['user'].value_counts().head()

    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'count': 'percent' , 'user': 'name'})
    return x,df
    # name = x.index
    # count = x.values
    # plt.bar(name,count)


def create_wordcloud(selected_user,df):
    if selected_user !="overall":
        df = df[df['user'] == selected_user]
    
    new_df = df[df['message'] != '<Media omitted>']

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(new_df['message'].str.cat(sep=""))
    return df_wc

## most commont words
def most_common_words(selected_user,df):
    if selected_user !="overall":
        df = df[df['user'] == selected_user]

    new_df = df[df['message'] != '<Media omitted>']
    words = []
    for message in new_df['message']:
        words.extend(message.split())

    most_common_df = pd.DataFrame(Counter(words).most_common(40))
    return most_common_df

## emojis function

def extract_emojis(selected_user,df):
    if selected_user !="overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
    

    