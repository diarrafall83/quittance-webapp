from flask import Flask, render_template_string, render_template, redirect, url_for, make_response, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from weasyprint import HTML, CSS
import traceback
import os
from datetime import datetime
from urllib.parse import unquote

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

# ... all previous routes ...

@app.route("/quittance/<building>/pdf")
def quittance_merged_pdf(building):
    try:
        from weasyprint import HTML

        month = request.args.get("month", datetime.now().strftime("%B"))
        year = request.args.get("year", datetime.now().strftime("%Y"))

        sheet = get_gsheet()
        ws = sheet.worksheet(building)
        rows = ws.get_all_values()
        header = rows[0]

        blocks = []
        for i, row in enumerate(rows):
            if i == 0 or len(row) < len(header):
                continue
            try:
                tenant_data = enrich_tenant_data(building, dict(zip(header, row)), month, year)
                html_block = render_template("quittance.html", tenant=tenant_data, month_label=tenant_data['month_label'], footer_split=True)
                blocks.append(f"<div style='width:50%;padding:10px;'>{html_block}</div>")
            except Exception as inner:
                print(f"Error rendering row {i}: {inner}")
                continue

        double_per_page = "".join(
            f"<div style='display:flex;flex-direction:row;justify-content:space-between;page-break-after:always'>{blocks[i]}{blocks[i+1] if i+1 < len(blocks) else ''}</div>"
            for i in range(0, len(blocks), 2)
        )
        html_out = f"<html><body>{double_per_page}</body></html>"

        pdf = HTML(string=html_out, base_url=request.host_url).write_pdf(stylesheets=[CSS(string='@page { size: A4; margin: 1cm }')])
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f"inline; filename=quittances_{building}_{month}_{year}.pdf"
        return response

    except Exception as e:
        return f"<h3>Erreur PDF Global:</h3><pre>{traceback.format_exc()}</pre>"
