from flask import Flask, render_template, request
import requests
from datetime import datetime
import os

app = Flask(__name__)

AUTHOR = "Michał Choina"
PORT = 5000
API_KEY = os.getenv("API_KEY")

locations = {
    "Polska": ["Warszawa", "Kraków", "Lublin"],
    "Niemcy": ["Berlin", "Monachium"],
    "USA": ["New York", "Los Angeles"]
}

@app.route("/", methods=["GET", "POST"])
def index():
    selected_country = None
    cities = []
    weather = None

    if request.method == "POST":
        selected_country = request.form.get("country")
        selected_city = request.form.get("city")

        if selected_country and not selected_city:
            cities = locations.get(selected_country, [])

        if selected_country and selected_city:
            cities = locations.get(selected_country, [])

            url = f"http://api.openweathermap.org/data/2.5/weather?q={selected_city}&appid={API_KEY}&units=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                weather = {
                    "city": selected_city,
                    "temp": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"]
                }

    return render_template(
        "index.html",
        locations=locations,
        selected_country=selected_country,
        cities=cities,
        weather=weather
    )


if __name__ == "__main__":
    print("======================================")
    print(f"Data uruchomienia: {datetime.now()}")
    print(f"Autor: {AUTHOR}")
    print(f"Port: {PORT}")
    print("======================================")

    app.run(host="0.0.0.0", port=PORT)