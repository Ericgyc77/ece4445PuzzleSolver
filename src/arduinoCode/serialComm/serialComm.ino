void setup() {
  // Begin serial communication at a baud rate of 9600:
  // Can use baud rate of 9600 (need to adjust manually on Raspberry Pi) or just use default rate of 115200 
  Serial.begin(9600);
}

void loop() {
  // Check if data is available to read.
  if (Serial.available() > 0) {
    String data = Serial.readString(); // Read the incoming data as string

    // Echo the received data back to the serial.
    Serial.println("Arduino Received: " + data);
  }
  else {
    Serial.println("No incoming data detected.");
  }

  // Send a simple message every 2 seconds.
  Serial.println("Arduino Sent: Hello from Arduino!");
  delay(2000);
}