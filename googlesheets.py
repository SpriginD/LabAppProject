from __future__ import print_function
from pprint import pprint
from dotenv import load_dotenv
import sqlite3 as sq
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient import discovery

from google.oauth2 import service_account

load_dotenv()

COLORS = {
    frozenset({'red': 1, 'green': 1, 'blue': 1}.items()): None,
    frozenset({'red': 0.5764706, 'green': 0.76862746, 'blue': 0.49019608}.items()): "OK",
    frozenset({'red': 0.94509804, 'green': 0.7607843, 'blue': 0.19607843}.items()): "Warning",
    frozenset({'red': 0.8784314, 'green': 0.4, 'blue': 0.4}.items()): "Problem"
}

basedir = os.path.abspath(os.path.dirname(__file__))

SERVICE_ACCOUNT_FILE = os.path.join(basedir, os.getenv('SERVICE_ACCOUNT_FILE'))
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

credentials = None

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = os.getenv('SAMPLE_SPREADSHEET_ID')
SAMPLE_RANGE_NAME = os.getenv('SAMPLE_SPREADSHEET_ID')
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.

def UpdateDatabase():
    con = sq.connect("googlesheetsdatas.db")
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS pc")
    cur.execute("""CREATE TABLE "pc" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "state"	TEXT,
                    "vstudio"	TEXT,
                    "problem"	TEXT,
                    "solution"	TEXT,
                    PRIMARY KEY("id")
                )""")

    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    result = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, ranges=SAMPLE_RANGE_NAME, includeGridData=True).execute()
    rows = result["sheets"][0].get("data")[0]["rowData"]

    for row in rows:
        rowData = []
        for value in row["values"]:
            cell_name = ""
            cell_bg_color = None
            state = None

            if value.get("userEnteredValue"):
                cell_name = value.get("userEnteredValue").get(list(value.get("userEnteredValue").keys())[0])
            else:
                if value.get("effectiveFormat") and isinstance(value.get("effectiveFormat"), dict):
                    cell_bg_color = frozenset(value.get("effectiveFormat").get("backgroundColor").items())
            
                if cell_bg_color:
                    state = COLORS[cell_bg_color]

            if state:
                rowData.append(state)
                continue
            else:
                rowData.append(cell_name)

        if len(rowData) != 5:
            for i in range(5-len(rowData)):
                rowData.append("")

        cur.execute("INSERT INTO pc VALUES(?, ?, ?, ?, ?)", tuple(rowData))

    con.commit()
    con.close()

    print("DATABASE UPDATED")