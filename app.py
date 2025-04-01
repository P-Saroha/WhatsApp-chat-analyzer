import streamlit as st
import preprocessor , helper

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt"])

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")  # decoding
    df = preprocessor.preprocess(data)

    st.dataframe(df)
    
    # fetching unique users 

    user_list = df['user'].unique().tolist()

    user_list.sort()
    user_list.insert(0,"overall")

    st.sidebar.subheader("Select a user:")
    selected_user = st.sidebar.selectbox("Users", user_list)

    if st.sidebar.button("show analytics"):

        num_messages, words, no_of_media_messages, num_of_links = helper.fetch_stats(selected_user,df)
        
        col1, col2, col3, col4 = st.columns(4)

    
        with  col1:
            st.header("Total Message")
            st.text(num_messages)

        with  col2:
            st.header("Total Words")
            st.text(words)
        
        with  col3:
            st.header("Media Shared")
            st.text(no_of_media_messages)

        with  col4:
            st.header("No. of Link Shared")
            st.text(num_of_links)


        # finding the busiest users in the groups
        if selected_user != "overall":
            st.subheader("Busiest Users")
            busiest_users = df[df['user'] == selected_user].groupby('user')['message'].count().reset_index().nlargest(5, 'message')
            st.dataframe(busiest_users)