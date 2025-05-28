# IoT Temperature Monitoring with ESP32, MQTT, and Telegram

📡 ESP32 + LM35 sensor reads ambient temperature  
🌐 Sends data to a public MQTT broker (`broker.emqx.io`)  
🤖 A Python bot deployed on Render.com listens and sends alerts to Telegram

## Features

- ESP32 reads analog temperature from LM35
- Publishes to MQTT topic: `sensors/temperature`
- Python bot on Render.com receives temperature and sends to Telegram if needed

## Files

- `esp32_mqtt_temp.ino` — Arduino code for ESP32
- `mqtt_telegram_bot.py` — Python Telegram bot (Render-ready)
- `requirements.txt` — Dependencies for the bot

## Example alert

🚨 Температура высокая: 32.75 °C

## Deployment

ESP32 → MQTT (EMQX) → Python bot (Render) → Telegram 💬