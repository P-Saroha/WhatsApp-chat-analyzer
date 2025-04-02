import streamlit as st
import preprocessor , helper
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt"])

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")  # decoding
    df = preprocessor.preprocess(data)

    # st.dataframe(df)
    
    # fetching unique users 

    user_list = df['user'].unique().tolist()

    user_list.sort()
    user_list.insert(0,"overall")

    st.sidebar.subheader("Select a user:")
    selected_user = st.sidebar.selectbox("Users", user_list)

    if st.sidebar.button("show analytics"):

        num_messages, words, no_of_media_messages, num_of_links = helper.fetch_stats(selected_user,df)

        st.header("Chat Analysis") #####
        
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
        if selected_user == "overall":
            st.subheader("Most Busiest Users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical') 
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
        # WordCloud
        st.subheader("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)



        ## monthely timeline of messages 

        st.subheader("Monthly Chat Analysis")
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax =  plt.subplots()
        plt.plot(timeline['time'],timeline['message'],color = 'orange' )
        plt.xticks(rotation='vertical')
        # plt.show()
        st.pyplot(fig)

        ## Daily timeline 
        st.subheader("Daily Chat Analysis")

        daily_timeline = helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots(figsize=(18, 12))  
        # plt.figure(figsize=(12,6))
        plt.xticks(rotation='vertical')
        plt.plot(daily_timeline['message_in_a_day'],daily_timeline['message'],color = "green")
        st.pyplot(fig)

        ## weekely chat 
        st.subheader("Weekely Activity Chat Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Most Busy day")

            weekely_chat = helper.weekly_chat(selected_user,df)
            fig,ax = plt.subplots(figsize=(10, 6))
            plt.xticks(rotation='vertical')
            ax.bar(weekely_chat.index,weekely_chat.values)
            st.pyplot(fig)

        with col2:
            st.subheader("Most Busy Month")

            month_activity = helper.month_activity(selected_user,df)
            fig,ax = plt.subplots(figsize=(10, 6))
            plt.xticks(rotation='vertical')
            ax.bar(month_activity.index,month_activity.values,color= "pink")
            st.pyplot(fig)


        ########### Heat map ############
        st.subheader("Weekly Activity HeatMap")

        # Get heatmap data
        user_heatmap = helper.chat_heatmap(selected_user, df)

        # Set proper figure size
        fig, ax = plt.subplots(figsize=(10, 6))  

        # Use a better colormap & improve visibility
        sns.heatmap(user_heatmap, ax=ax, cmap="Blues", annot=True, fmt=".0f", linewidths=0.5)

        # Improve x-axis & y-axis label alignment
        ax.set_xlabel("Hour of the Day")
        ax.set_ylabel("Day of the Week")
        ax.set_title("User Weekly Activity Heatmap", fontsize=14)

        # Display plot
        st.pyplot(fig)

       


        ## most common words 

        most_common_df = helper.most_common_words(selected_user,df)
        st.subheader("Most Common Words")

        fig, ax = plt.subplots(figsize=(14, 10))

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation = 'vertical')

        st.pyplot(fig)
        # st.dataframe(most_common_df)

        ## emojis analysis
        emoji_df = helper.extract_emojis(selected_user,df)

        st.subheader("Emojis Analysis")
        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        top_5_emojis = emoji_df.head(5)  # Get top 5 emojis
        # Set the font to one that supports emojis
        mpl.rcParams['font.family'] = 'Noto Color Emoji'

        with col2:
            fig, ax = plt.subplots()
            ax.pie(top_5_emojis[1], labels=top_5_emojis[0], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.title('Top 5 Emojis')

            # Display the pie chart
            st.pyplot(fig)


