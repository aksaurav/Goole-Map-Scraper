""" Google Sheets Integration"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv

# Define the scope and credentials file path
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
credentials_path = "uplifted-time-269814-92549a3043e6.json"

# Authenticate
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
gc = gspread.authorize(credentials)

# Open the Google Sheets document
spreadsheet_key = "1UTCc5jnghwR1MDmlZ4Nj59eeuO_xxjpKpTKTLcT8fU8"
worksheet = gc.open_by_key(spreadsheet_key).sheet1  # Open the first sheet

# Read data from the CSV file
csv_file_path = "D:\\Coding_Projects\\assignment\\google_map_business_data.csv"
with open(csv_file_path, mode="r", encoding="utf-8") as file:
    csv_reader = csv.reader(file)
    data_to_append = list(csv_reader)

# Append the data
worksheet.append_rows(data_to_append)

print("Data from CSV appended successfully!")
