#include <WiFi.h>
#include <PubSubClient.h>

// Wi-Fi
const char* ssid = "iPhone";
const char* password = "neda2331";

// MQTT
const char* mqtt_server = "broker.emqx.io";
const int mqtt_port = 1883;
const char* mqtt_user = "";
const char* mqtt_pass = "";
const char* topic = "sensors/temperature";

WiFiClient espClient;
PubSubClient mqttClient(espClient);

// LM35 на VN (GPIO39)
const int sensorPin = 39;

void setup_wifi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
}

void reconnectMQTT() {
  while (!mqttClient.connected()) {
    if (mqttClient.connect("ESP32Client", mqtt_user, mqtt_pass)) {
      Serial.println("MQTT connected");
    } else {
      delay(5000);
    }
  }
}

float readTemperature() {
  long sum = 0;
  const int samples = 10;
  for (int i = 0; i < samples; i++) {
    sum += analogRead(sensorPin);
    delay(10);
  }
  float avg = sum / samples;
  float voltage = avg * (3.3 / 4095.0);
  return voltage * 100.0;
}

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  setup_wifi();
  mqttClient.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!mqttClient.connected()) reconnectMQTT();
  mqttClient.loop();

  float temperature = readTemperature();
  char msg[50];
  snprintf(msg, 50, "%.2f", temperature);
  mqttClient.publish(topic, msg);
  Serial.println("Published to MQTT");

  delay(20000);
}
