import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    # Define pattern for timestamps (Handles both 12-hour AM/PM and 24-hour formats)
    pattern = r"(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}(?:\s?[APap][Mm])?) - (.+)"
    
    # Extract all matches
    matches = re.findall(pattern, data)

    # Lists to store extracted data
    users = []
    messages = []
    datetimes = []

    for match in matches:
        date_part, time_part, msg = match  # Unpacking tuple
        
        # **Remove encryption message**
        if "Messages and calls are end-to-end encrypted" in msg:
            continue  # Skip encryption messages

        # **Fix space issue in AM/PM timestamps**
        time_part = time_part.replace("\u202F", " ")  # Replace narrow space with a regular space

        # **Split user and message**
        split_msg = msg.split(": ", 1)  
        if len(split_msg) == 2:
            user, message = split_msg
        else:
            user = "Unknown"
            message = split_msg[0]

        # # **Replace "." with "PK"**
        # if user == ".":
        #     user = "PK"

        # **Handle 12-hour and 24-hour formats**
        formatted_datetime = None
        for fmt in ("%d/%m/%y %H:%M", "%d/%m/%y %I:%M %p", "%d/%m/%Y %H:%M", "%d/%m/%Y %I:%M %p"):
            try:
                formatted_datetime = datetime.strptime(f"{date_part} {time_part}", fmt)
                break  # If parsing succeeds, exit loop
            except ValueError:
                continue  # Try the next format
        
        if formatted_datetime is None:
            continue  # Skip if parsing fails

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

    # Extracting additional time details
    chat_df['year'] = chat_df['datetime'].dt.year
    chat_df['month_num'] = chat_df['datetime'].dt.month
    chat_df['month'] = chat_df['datetime'].dt.month_name()
    chat_df['message_in_a_day'] = chat_df['datetime'].dt.date
    chat_df['day_name'] = chat_df['datetime'].dt.day_name()
    chat_df['day'] = chat_df['datetime'].dt.day
    chat_df['hour'] = chat_df['datetime'].dt.hour
    chat_df['minute'] = chat_df['datetime'].dt.minute

    # Define message period (e.g., "10-11 AM")
    period = []
    for hour in chat_df['hour']:
        if hour == 23:
            period.append("23-00")
        elif hour == 0:
            period.append("00-01")
        else:
            period.append(f"{hour}-{hour+1}")

    chat_df['period'] = period

    return chat_df  
