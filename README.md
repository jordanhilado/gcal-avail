# Google Calendar Availability Exporter

Script that exports your availability based off of times in which events are not scheduled on your primary Google Calendar.

## Example

```
> python3 avail.py
How many events far out do you want to see? 20
- Friday, 11/11: 12:00am-8:00am, 8:30am-11:59pm
- Monday, 11/14: 12:00am-9:00am, 10:45am-3:30pm, 4:45pm-5:00pm, 6:15pm-7:00pm, 8:00pm-11:59pm
- Tuesday, 11/15: 12:00am-11:00am, 12:15pm-12:30pm, 1:45pm-3:00pm, 5:00pm-5:30pm, 6:45pm-11:59pm
- Wednesday, 11/16: 12:00am-9:30am, 10:45am-3:30pm, 4:45pm-5:00pm, 6:15pm-7:00pm, 7:30pm-11:59pm
- Thursday, 11/17: 12:00am-11:00am, 12:15pm-12:30pm, 1:45pm-3:00pm, 4:00pm-5:00pm, 6:45pm-11:59pm
```

## Local Setup

1. Follow the [Google Calendar API Python quickstart](https://link-url-here.org) documentation steps
2. After full setup, run the `avail.py` file in the same directory where your `credentials.json` is located
