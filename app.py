from flask import Flask, render_template_string
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

@app.route("/")
def home():
    # Connect to Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("/etc/secrets/credentials.json", scope)
    client = gspread.authorize(creds)

    # Open your spreadsheet by ID
    sheet_id = "1zZExWm-Kzdcf41ua9M7Njwo1gMp9jy7H"
    sheet = client.open_by_key(sheet_id)
    ws = sheet.get_worksheet(0)  # First worksheet

    # Read rows
    rows = ws.get_all_values()

    # Display them
    html = "<h2>Liste des locataires</h2><table border='1'>"
    for row in rows:
        html += "<tr>" + "".join([f"<td>{cell}</td>" for cell in row]) + "</tr>"
    html += "</table>"

    return render_template_string(html)
