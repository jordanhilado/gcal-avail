from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
TIME_ZONE_OPTIONS = {
    "PST": "America/Los_Angeles",
    "MST": "America/Phoenix",
    "CST": "America/Chicago",
    "EST": "America/New_York",
}

def calculate_end_date(x):
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    days_added = 0
    while days_added < x:
        if tomorrow.weekday() not in (5, 6):  # Not weekend
            days_added += 1
        tomorrow += datetime.timedelta(days=1)
    return tomorrow.strftime("%Y-%m-%d")


def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("calendar", "v3", credentials=creds)

        while True:
            time_zone = input(
                "Enter your desired time zone (PST, MST, CST, EST): "
            ).upper()
            if time_zone in TIME_ZONE_OPTIONS:
                break
            else:
                print(
                    "Invalid time zone. Please choose from the following: PST, MST, CST, or EST."
                )

        while True:
            try:
                days = int(
                    input(
                        "How many days out do you want to see your availability? "
                    )
                )
                if days > 0:
                    break
                else:
                    print("Invalid input. Please enter a positive integer.")
            except ValueError:
                print("Invalid input. Please enter a positive integer.")

        time_zone_offset = TIME_ZONE_OPTIONS[time_zone]

        end_date = (datetime.datetime.now() + datetime.timedelta(days=days + 1)).isoformat()
        end_date = end_date.split("T")[0] + "T07:00:00Z"

        event_list = (
            service.events()
            .list(
                calendarId="primary",
                singleEvents=True,
                timeMin=datetime.datetime.now().isoformat() + "Z",
                timeMax=end_date,
                timeZone=time_zone_offset,
                orderBy="startTime",
            )
            .execute()
        )

        events = event_list.get("items", [])

        if not events:
            print('No upcoming events found.')
            return

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
        
        avail = {}
        for d, t in eventDict.items():
            start = '09:00'
            end = '21:00'
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
                # subtract both times
                start = datetime.datetime.strptime(i[0], '%H:%M')
                end = datetime.datetime.strptime(i[1], '%H:%M')
                diff = end - start
                # check if diff is greater than 30 min
                if diff.seconds < 1800:
                    break
                start, end = datetime.datetime.strptime(i[0], "%H:%M").strftime("%I:%M %p"), datetime.datetime.strptime(i[1], "%H:%M").strftime("%I:%M %p")
                timeArr.append(start.replace(" ", "").strip("0").lower().strip() + "-" + end.replace(" ", "").strip("0").lower().strip())
            timeStr = ", ".join(timeArr)
            if timeStr == '':
                continue
            print("- " + weekday + ", " + month + "/" + day + ": " + timeStr)

    except HttpError as error:
        print("An error occurred: %s" % error)


if __name__ == "__main__":
    main()
