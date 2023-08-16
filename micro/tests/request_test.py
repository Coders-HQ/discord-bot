import requests

body = {
  "title" : "EKoders - Sales Force",
  "image": "https://codershq0.blob.core.windows.net/media/event/image/e-koders-sales-force_sIJIj6B.jpg",
  "date_time": "2023-08-17 20:00",
  "duration": 3,
  "short_description": "Salesforce seminars series provided by EK koders(Emirates Airlines)",
  "event_link": "",
  "event_location" : "Coders HQ, Emirates Towers, Dubai",
  "seats" : 15
}
resp = requests.post('http://127.0.0.1:8000/bot/event',json=body)