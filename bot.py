import asyncio
from telegram import Bot
from paho.mqtt.client import Client as MQTTClient

# MQTT настройки
MQTT_BROKER = "172.20.10.2"
MQTT_PORT = 1883
MQTT_TOPIC = "sensors/temperature"

# Telegram настройки
TELEGRAM_TOKEN = "8033945829:AAEZ9GB12aN76EZLWFZH5HOH1cdCm4KgeCU"
CHAT_ID = "266889430"
bot = Bot(token=TELEGRAM_TOKEN)

# Очередь и loop
message_queue = asyncio.Queue()
event_loop = None  # глобальная переменная под event loop


def on_mqtt_message(client, userdata, msg):
    global event_loop
    try:
        temp = float(msg.payload.decode())
        print(f"[MQTT] Temp received: {temp:.2f}°C")
        if temp > 10.0:
            # Передача задачи в event loop
            asyncio.run_coroutine_threadsafe(
                message_queue.put(f"🚨 Температура высокая: {temp:.2f} °C"),
                event_loop
            )
    except Exception as e:
        print("[MQTT] Error:", e)


async def telegram_worker():
    while True:
        message = await message_queue.get()
        try:
            await bot.send_message(chat_id=CHAT_ID, text=message)
            print("[BOT] Telegram alert sent!")
        except Exception as e:
            print("[BOT] Telegram failed:", e)


async def main():
    global event_loop
    event_loop = asyncio.get_running_loop()  # сохранить текущий loop

    # MQTT подключение
    mqtt_client = MQTTClient()
    mqtt_client.on_message = on_mqtt_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
    mqtt_client.subscribe(MQTT_TOPIC)
    mqtt_client.loop_start()

    print("[MQTT] Subscribed and listening...")

    # Старт Telegram-воркера
    await telegram_worker()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[EXIT] Stopped by user")
