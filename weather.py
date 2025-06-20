import requests
import smtplib
from email.message import EmailMessage
import schedule
import time

# === CONFIG ===
API_KEY = 'b73b027b6fbf9620226a8b4cbdc52972'  # Your OpenWeatherMap API Key
CITY = 'Kigali'
EMAIL_SENDER = 'emmychris915@gmail.com'
EMAIL_PASSWORD = 'qtun jtji plqw ppkv'  # Gmail App Password (not regular password)
EMAIL_SMTP_SERVER = 'smtp.gmail.com'
EMAIL_SMTP_PORT = 587
RECIPIENTS = [
    'kubwimanatheophile02@gmail.com',
    'muhayimanaemilien@gmail.com',
    'basesayosejmv@gmail.com'
]

# === FUNCTION TO GET WEATHER ===
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    print("API response:", data)  # Debug line

    if response.status_code != 200 or 'main' not in data:
        raise Exception(f"API error: {data.get('message', 'Unknown error')}")

    temp = data['main']['temp']
    description = data['weather'][0]['description']
    humidity = data['main']['humidity']
    wind = data['wind']['speed']

    return temp, description, humidity, wind

# === FUNCTION TO SEND EMAIL ===
def send_email(subject, plain_text, html_content, to_emails):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = ', '.join(to_emails)
    msg.set_content(plain_text)
    msg.add_alternative(html_content, subtype='html')

    with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

# === MAIN FUNCTION TO RUN EMAIL ===
def run_weather_email():
    print("⏳ Fetching weather...")
    try:
        temp, desc, humidity, wind = get_weather(CITY)

        # Plain text fallback
        plain_text = (f"Weather Forecast for {CITY}:\n"
                      f"- Temperature: {temp}°C\n"
                      f"- Condition: {desc.capitalize()}\n"
                      f"- Humidity: {humidity}%\n"
                      f"- Wind Speed: {wind} m/s\n")

        # HTML version
        html_content = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background: #f2f2f2; padding: 20px;">
            <div style="max-width: 500px; margin: auto; background: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
              <h2 style="color: #2E86C1;">🌤 Daily Weather Forecast for {CITY}</h2>
              <ul style="list-style-type: none; padding: 0;">
                <li><strong>🌡 Temperature:</strong> {temp}°C</li>
                <li><strong>☁ Condition:</strong> {desc.capitalize()}</li>
                <li><strong>💧 Humidity:</strong> {humidity}%</li>
                <li><strong>🌬 Wind Speed:</strong> {wind} m/s</li>
              </ul>
              <p style="font-size: 0.9em; color: #888;">Stay safe and dress accordingly. 🚶‍♂️☂️</p>
            </div>
          </body>
        </html>
        """

        print("📧 Sending email...")
        send_email("Daily Weather Forecast 🌤", plain_text, html_content, RECIPIENTS)
        print("✅ Email sent successfully!")

    except Exception as e:
        print(f"⚠️ Error occurred: {e}")

# === RUN ONCE IMMEDIATELY (for testing) ===
run_weather_email()

# === SCHEDULE TO RUN DAILY AT 07:00 AM ===
schedule.every().day.at("07:00").do(run_weather_email)

# === KEEP SCRIPT RUNNING TO CHECK SCHEDULE ===
while True:
    schedule.run_pending()
    time.sleep(60)
