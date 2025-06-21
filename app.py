from flask import Flask, render_template_string, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

def get_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("/etc/secrets/credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open_by_key("1mvEss9g3h1-Fekf9tWt41_GoaK6DStP2GmtT96v1hMY")

@app.route("/")
def list_buildings():
    try:
        sheet = get_gsheet()
        tabs = sheet.worksheets()
        html = "<h2>🏢 Sélectionner un bâtiment</h2><ul>"
        for tab in tabs:
            html += f"<li><a href='/building/{tab.title}'>{tab.title}</a></li>"
        html += "</ul>"
        return render_template_string(html)
    except Exception as e:
        return f"<h3>Erreur Google Sheet:</h3><pre>{str(e)}</pre>"

@app.route("/building/<name>")
def show_building(name):
    try:
        sheet = get_gsheet()
        ws = sheet.worksheet(name)
        rows = ws.get_all_values()
        html = f"<h2>👥 Locataires - {name}</h2><table border='1'>"
        for row in rows:
            html += "<tr>" + "".join([f"<td>{cell}</td>" for cell in row]) + "</tr>"
        html += "</table><br><a href='/'>← Retour</a>"
        return render_template_string(html)
    except Exception as e:
        return f"<h3>Erreur: {name}</h3><pre>{str(e)}</pre>"


