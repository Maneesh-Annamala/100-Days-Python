from datetime import datetime
import pandas
import random
import smtplib

# Sender email credentials
MY_EMAIL = "YOUR EMAIL"
MY_PASSWORD = "YOUR PASSWORD"

# Get today's date
today = datetime.now()

# Store today's month and day as a tuple
today_tuple = (today.month, today.day)

# Read birthday data from CSV file
data = pandas.read_csv("birthdays.csv")

# Convert dataframe into dictionary for faster lookup
birthdays_dict = {
    (data_row["month"], data_row["day"]): data_row
    for (index, data_row) in data.iterrows()
}

# Check if today matches any birthday
if today_tuple in birthdays_dict:

    # Get today's birthday person's details
    birthday_person = birthdays_dict[today_tuple]

    # Randomly select one birthday letter template
    file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"

    # Read the selected letter
    with open(file_path) as letter_file:

        contents = letter_file.read()

        # Replace placeholder with person's name
        contents = contents.replace("[NAME]", birthday_person["name"])

    # Connect to SMTP server
    with smtplib.SMTP("YOUR EMAIL PROVIDER SMTP SERVER ADDRESS") as connection:

        # Secure the connection
        connection.starttls()

        # Login to sender account
        connection.login(MY_EMAIL, MY_PASSWORD)

        # Send birthday email
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=birthday_person["email"],
            msg=f"Subject:Happy Birthday!\n\n{contents}"
        )