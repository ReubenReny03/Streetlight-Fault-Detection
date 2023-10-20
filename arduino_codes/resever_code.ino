#include <SPI.h>
#include <LoRa.h>

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!LoRa.begin(915E6)) {
    Serial.println("LoRa initialization failed. Check your wiring.");
    while (1);
  }
  
}

String last_msg = "100";
void loop() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    String receivedMessage = "";
    while (LoRa.available()) {
      receivedMessage += (char)LoRa.read();
    }
    Serial.println(receivedMessage);
    last_msg = receivedMessage;
  }
  else{
    Serial.println(last_msg);
  }
  delay(500);
}
