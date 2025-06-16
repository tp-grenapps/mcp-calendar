import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from dotenv import load_dotenv
 
 
load_dotenv()
 
cred_file=os.getenv("CRED_FILE")
token_file = os.getenv("TOKEN_FILE")

# If modifying these scopes, delete the file token.json
SCOPES = [
          "https://www.googleapis.com/auth/calendar.readonly",
          "https://www.googleapis.com/auth/calendar",
          'https://www.googleapis.com/auth/calendar.events'
          ]


class GoogleCalendarAPI:
    def __init__(self, credentials_file: str = cred_file, token_file: str = token_file):
        """
        Initialize Google Mail API client
        
        Args:
            credentials_file: Path to your OAuth2 credentials JSON file
            token_file: Path to store the access token
        """
        self.Scopes = SCOPES
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Handle OAuth2 authentication"""
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.Scopes)
            
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    cred_file, SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_file, "w") as token:
                token.write(creds.to_json())
        
        # Build the service
        self.service = build("calendar", "v3", credentials=creds)
        
        print("Successfully authenticated with Google Calendar API!")  
      
    def list_items(self):
        try:
        
            # Call the Calendar API
            now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
            print("Getting the upcoming 10 events")
            events_result = (
                self.service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                print("No upcoming events found.")
                return

            # Prints the start and name of the next 10 events
            event_list=[]
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])
                event_list.append({
                  "Time": start,
                  "Description": event["summary"]
                })
            return event_list

        except HttpError as error:
            print(f"An error occurred: {error}")
            return None 
    
    def add_event(self, event=None):
      
      eventx = {
        'summary':event['summary'],
        'location':event['location'],
        'description':event['description'],
        'start': {
          'dateTime': event["startTime"],
          'timeZone': 'Asia/Kuala_Lumpur',
        },
        'end': {
          'dateTime': event["endTime"],
          'timeZone': 'Asia/Kuala_Lumpur',
        },
      }

      event = self.service.events().insert(calendarId='primary', body=eventx).execute()

  

def main():
    cal_api = GoogleCalendarAPI()
    print(cal_api.list_items())
    
if __name__ == "__main__":
  main()