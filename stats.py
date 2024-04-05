from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
import os
import pickle
import pandas as pd

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/drive"]

def groupBy(df):
    return df.groupby("Category").sum()

def main():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("drive", "v3", credentials=creds)

    file_id = "1ifGqJM-h4us8FaikgXxyDCrcywtmvHLA-IvxCo7aNrQ"
    request = service.files().export_media(fileId=file_id, mimeType='text/csv')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

    l = fh.getvalue().decode("utf-8").split("\r\n")
    l = [x.split(",") for x in l]
    df = pd.DataFrame(l, columns=["Date", "Amount", "Purchase", "Category", "Split"])
    df = df["Amount"].astype(int)
    df = df["Split"].astype(int)
    print(groupBy(df))

if __name__ == "__main__":
    main()
