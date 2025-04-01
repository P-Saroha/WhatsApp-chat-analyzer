from urlextract import URLExtract
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

        

