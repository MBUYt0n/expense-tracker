from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
import os
import pickle

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/drive"]


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

    with open("downloaded_file.txt", "wb") as out_file:
        out_file.write(fh.getvalue())
    print('Downloaded file has been saved as "downloaded_file.txt"')

    file_id1 = "1_bhKM85tnUnDvq7aj3lYGihzps6LeNxIAcCz23tAaPY"

    request = service.files().export_media(fileId=file_id1, mimeType="text/plain")
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    with open('downloaded_file.txt', 'a') as out_file:
        out_file.write("\n")
        out_file.write(fh.getvalue().decode('utf-8'))

    empty_file_metadata = {"name": "Expenses", "mimeType": "text/plain"}
    empty_media = MediaFileUpload(
        "empty_file.txt", mimetype="text/plain", resumable=True
    )
    empty_file = (
        service.files()
        .update(fileId=file_id1, body=empty_file_metadata, media_body=empty_media)
        .execute()
    )
    print("The file has been truncated. File ID: %s" % empty_file.get("id"))
    
    file_metadata = {
        "name": "expenses.csv",
        "mimeType": "application/vnd.google-apps.spreadsheet",
    }
    media = MediaFileUpload('downloaded_file.txt', mimetype='text/csv', resumable=True)
    file = service.files().update(fileId=file_id, body=file_metadata, media_body=media, fields='id').execute()
    print("File ID: %s" % file.get('id'))

    os.remove("downloaded_file.txt")


if __name__ == "__main__":
    main()
