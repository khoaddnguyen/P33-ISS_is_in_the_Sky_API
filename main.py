# send email to user when the ISS is close to their current position
# code runs every 60 secs
import requests
from datetime import datetime
import smtplib

MY_EMAIL = "aaa@gmail.com"
MY_PASSWORD = "password"

MY_LAT = 30.264980  # Your latitude
MY_LONG = -97.746597  # Your longitude

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your current position is within +5 or -5 degrees of the ISS position
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    print(sunrise)
    print(sunset)

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True

if is_iss_overhead() and is_night():
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(MY_EMAIL, MY_PASSWORD)
    connection.sendmail(
        from_addr=MY_EMAIL,
        to_addrs=MY_EMAIL,
        msg="Subject: Look Up \n\n The ISS is above you in the sky :)"
    )
# send an email when ISS is overhead and when it's dark so they can see the ISS in the sky

