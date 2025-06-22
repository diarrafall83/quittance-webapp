from flask import Flask, render_template_string, render_template, redirect, url_for, make_response, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from weasyprint import HTML
import traceback
import os
from datetime import datetime

app = Flask(__name__)

def get_gsheet():
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        path = "/etc/secrets/credentials.json"
        if not os.path.exists(path):
            raise FileNotFoundError(f"Credentials not found at {path}")

        creds = ServiceAccountCredentials.from_json_keyfile_name(path, scope)
        client = gspread.authorize(creds)
        return client.open_by_key("1mvEss9g3h1-Fekf9tWt41_GoaK6DStP2GmtT96v1hMY")
    except Exception as e:
        raise RuntimeError(f"🔴 get_gsheet() error:\n{traceback.format_exc()}")

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
        return f"<h3>Erreur Google Sheet:</h3><pre>{e}</pre>"

# Existing routes (building, quittance generation, PDF, batch) remain unchanged below...
# [content truncated for brevity]
