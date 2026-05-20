from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    forecast = None
    error = None

    city = "Warsaw"

    if request.method == "POST":
        city = request.form.get("city")

    try:
        # Aktualna pogoda
        current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        current_response = requests.get(current_url)
        current_data = current_response.json()

        if current_response.status_code != 200:
            error = "Nie znaleziono miasta."
            return render_template("index.html", error=error)

        # Prognoza 7 dni
        lat = current_data["coord"]["lat"]
        lon = current_data["coord"]["lon"]

        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        weather = {
            "city": current_data["name"],
            "temperature": current_data["main"]["temp"],
            "description": current_data["weather"][0]["description"],
            "humidity": current_data["main"]["humidity"],
            "wind": current_data["wind"]["speed"],
            "icon": current_data["weather"][0]["icon"]
        }

        forecast = forecast_data["list"][:7]

    except Exception as e:
        error = "Wystąpił błąd podczas pobierania danych."

    return render_template(
        "index.html",
        weather=weather,
        forecast=forecast,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)