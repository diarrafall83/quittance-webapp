from flask import Flask, render_template_string
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

@app.route("/")
def home():
    try:
        # Setup Google Sheets API access
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("/etc/secrets/credentials.json", scope)
        client = gspread.authorize(creds)

        # Open your Google Sheet by ID
        sheet_id = "1zZExWm-Kzdcf41ua9M7Njwo1gMp9jy7H"
        sheet = client.open_by_key(sheet_id)

        # Use the first worksheet
        worksheet = sheet.get_worksheet(0)
        data = worksheet.get_all_values()

        # Build simple HTML to show tenant rows
        html = "<h2>Locataires</h2><table border='1' cellpadding='5'>"
        for row in data:
            html += "<tr>" + "".join([f"<td>{cell}</td>" for cell in row]) + "</tr>"
        html += "</table>"

        return render_template_string(html)

    except Exception as e:
        return f"<h2>Erreur de connexion Google Sheets</h2><pre>{str(e)}</pre>"
