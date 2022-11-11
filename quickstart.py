from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


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

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # print('Getting the upcoming 10 events')
        num_input = int(input("How many events far out do you want to see? "))
        events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=num_input, singleEvents=True, orderBy='startTime').execute()
        # print(type(events_result))
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        eventDict = {}
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            date = start[:10]
            startTime = start[11:16]
            endTime = end[11:16]
            if date not in eventDict:
                eventDict[date] = [(startTime, endTime)]
            else:
                eventDict[date].append((startTime, endTime))
            # print(start + " | " + end + " | " + event['summary'])

        # calculate availability
        avail = {}
        for d, t in eventDict.items():
            start = '00:00'
            end = '23:59'
            for s, e in t:
                if s > start:
                    if d not in avail:
                        avail[d] = [(start, s)]
                    else:
                        avail[d].append((start, s))
                start = e
            if start != end:
                if d not in avail:
                    avail[d] = [(start, end)]
                else:
                    avail[d].append((start, end))

        # print availability
        for date, times in avail.items():
            year, month, day = date.split('-')
            weekday = datetime.date(int(year), int(month), int(day)).strftime("%A")
            timeArr = []
            for i in times:
                if i[0] == '' or i[1] == '':
                    break
                start, end = datetime.datetime.strptime(i[0], "%H:%M").strftime("%I:%M %p"), datetime.datetime.strptime(i[1], "%H:%M").strftime("%I:%M %p")
                timeArr.append(start.replace(" ", "").strip("0").lower().strip() + "-" + end.replace(" ", "").strip("0").lower().strip())
            timeStr = ", ".join(timeArr)
            if timeStr == '':
                continue
            print("- " + weekday + ", " + month + "/" + day + ": " + timeStr)


    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()