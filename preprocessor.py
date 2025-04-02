import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    # Define pattern for timestamps
    pattern = r"(\d{1,2}/\d{1,2}/\d{4}), (\d{1,2}:\d{2}) - (.+)"

    # Extract all matches
    matches = re.findall(pattern, data)

    # Lists to store extracted data
    users = []
    messages = []
    datetimes = []

    for match in matches:
        date_part, time_part, msg = match  # Unpacking the tuple
        
        # Split user and message
        split_msg = msg.split(": ", 1)  # Splitting on first ': ' to separate user and message
        if len(split_msg) == 2:
            user, message = split_msg
        else:
            user = "Unknown"  # Handle system messages
            message = split_msg[0]

        # **Filter out system messages**
        if "Messages and calls are end-to-end encrypted" in message:
            continue  # Skip encryption messages

        # Correct datetime conversion
        formatted_datetime = datetime.strptime(f"{date_part} {time_part}", "%d/%m/%Y %H:%M")

        # Append to lists
        users.append(user)
        messages.append(message)
        datetimes.append(formatted_datetime)

    # Create DataFrame
    chat_df = pd.DataFrame({
        "datetime": datetimes,
        "user": users,
        "message": messages
    })

    # Replace "." with "PK" in user column
    # chat_df.loc[chat_df['user'] == '.', 'user'] = 'PK'
    chat_df['user'] = chat_df['user'].replace('.', 'PK')


    # Extracting additional time details
    chat_df['year'] = chat_df['datetime'].dt.year
    chat_df['month_num'] = chat_df['datetime'].dt.month
    chat_df['month'] = chat_df['datetime'].dt.month_name()
    chat_df['message_in_a_day'] = chat_df['datetime'].dt.date
    chat_df['day_name'] = chat_df['datetime'].dt.day_name()
    chat_df['day'] = chat_df['datetime'].dt.day
    chat_df['hour'] = chat_df['datetime'].dt.hour
    chat_df['minute'] = chat_df['datetime'].dt.minute

    period = []
    for hour in chat_df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    chat_df['period'] = period

    return chat_df  
