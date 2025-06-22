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
    return redirect(url_for('dashboard'))

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    try:
        month = request.form.get("month") or datetime.now().strftime("%B")
        year = request.form.get("year") or datetime.now().strftime("%Y")

        sheet = get_gsheet()
        total_buildings = 0
        total_tenants = 0
        total_rent = 0

        for ws in sheet.worksheets():
            rows = ws.get_all_values()
            total_buildings += 1
            total_tenants += len(rows) - 1
            header = rows[0]
            ttc_index = header.index("TTC") if "TTC" in header else -1
            if ttc_index >= 0:
                for row in rows[1:]:
                    try:
                        value = row[ttc_index].replace(" ", "").replace("FCFA", "")
                        total_rent += int(value)
                    except:
                        pass

        html = f"""
        <h1>📊 Tableau de Bord</h1>
        <form method='post'>
            Mois: <input name='month' value='{month}'>
            Année: <input name='year' value='{year}'>
            <button type='submit'>Filtrer</button>
        </form>
        <ul>
            <li>🏢 Nombre d'immeubles: <strong>{total_buildings}</strong></li>
            <li>👥 Total locataires: <strong>{total_tenants}</strong></li>
            <li>💰 Total TTC estimé pour {month} {year}: <strong>{total_rent:,} FCFA</strong></li>
        </ul>
        <a href='/'>← Voir la liste des bâtiments</a>
        """
        return render_template_string(html)
    except Exception as e:
        return f"<h3>Erreur Dashboard:</h3><pre>{e}</pre>"

# Existing routes (building, quittance generation, PDF, batch) remain unchanged below...
# [content truncated for brevity]
