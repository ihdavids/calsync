from __future__ import print_function
import datetime
from dateutil.parser import parse
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# 704863758352-f7gckoj2ep8i60oski22q7ucviareo9t.apps.googleusercontent.com
# TAN5Q20BcQPjSkvf5KEUFm6Q 

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=90, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    out = ""
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end   = event['end'].get('dateTime', event['end'].get('date'))
        start = parse(start)
        end = parse(end)
        summary = event['summary']
        desc = ""
        if('description' in event):
            desc    = event['description']
        out += "* {}\n".format(summary)
        if(start.time() != end.time()):
            out += "  " + start.strftime("<%Y-%m-%d %a %H:%M-") + end.strftime("%H:%M>") +"\n"
        else:
            out += "  " + start.strftime("<%Y-%m-%d %a %H:%M>") +"\n"
              
        out += "  " + desc + "\n"
        print(start, event['summary'])
    with open("cal.org","w",encoding='utf-8') as f:
        f.write(out)
    #print(str(events))


if __name__ == '__main__':
    main()