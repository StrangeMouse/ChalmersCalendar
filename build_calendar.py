import requests
from ics import Calendar
import re


ChalmersTimeEdit = "https://cloud.timeedit.net/chalmers/web/public/ri6372898yXZQ4Q8oZ5Qb6y05Z0Q250nQ0e0uyZQZY.ics"
guMedTimeEdit = "https://cloud.timeedit.net/gu/web/schema/ri6Q58221n7055QQ99Z66Y6Z0ZyQ8104.ics"

guMedCode = "EEN085"

all_events = []

chalmersData = requests.get(ChalmersTimeEdit)
chalmersC = Calendar(chalmersData.text)

guMedData = requests.get(guMedTimeEdit)
guMedC = Calendar(guMedData.text)

for chalmersE in chalmersC.events:
    kurs_match = re.search(r"Kurs namn:\s*([^,\.]+)", chalmersE.name)
    activity_match = re.search(r"Activity:\s*([^,\.]+)", chalmersE.name)

    kurskod_match = re.search(r"Kurs kod:\s*([^,\._]+)", chalmersE.name)

    ## print(kurskod_match.group(1) if kurskod_match else None)

    kurs_namn = kurs_match.group(1).strip() if kurs_match else None
    activity = activity_match.group(1).strip() if activity_match else None
    kurskod = kurskod_match.group(1).strip() if kurskod_match else None 

    chalmersE.name = f"{kurs_namn} - {activity}"  # change name to shorter version
    chalmersE.description = ""  # remove description


    if not kurskod == guMedCode:
        all_events.append(chalmersE)

for guMedEvent in guMedC.events:
    guMedEvent.name = f"Medicin för tekniker - {guMedEvent.name.split(",", 1)[1].strip()}"
    all_events.append(guMedEvent)


print(all_events)

# Write back
out_cal = Calendar(events=all_events)
with open("custom.ics", "w", encoding="utf-8") as f:
    f.writelines(out_cal)
