#include "AccelStepper.h"
#include <ezButton.h>

// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver:
#define dirPiny 2
#define stepPiny 3
#define dirPinx1 6
#define stepPinx1 7
#define dirPinx2 4
#define stepPinx2 5
#define motorInterfaceType 1

// constants won't change
// const int ENA_PIN = 9; // the Arduino pin connected to the EN1 pin L298N
const int IN1_PIN = 12; // the Arduino pin connected to the IN1 pin L298N
const int IN2_PIN = 13; // the Arduino pin connected to the IN2 pin L298N
const int SOL_PIN = 10;

// Create a new instance of the AccelStepper class:
AccelStepper stepperY = AccelStepper(motorInterfaceType, stepPiny, dirPiny);
AccelStepper stepperX1 = AccelStepper(motorInterfaceType, stepPinx1, dirPinx1);
AccelStepper stepperX2 = AccelStepper(motorInterfaceType, stepPinx2, dirPinx2);

ezButton limitSwitchY(8);  // create ezButton object that attach to pin 8, for the y stepper
ezButton limitSwitchX1(11);  // create ezButton object that attach to pin 11 this is for the left x stepper
ezButton limitSwitchX2(9);  // create ezButton object that attach to pin 9 this is for the right x stepper

bool startUpY;
bool startUpX1;
bool startUpX2;

/* 
  Destination Array Indicies to Corresponding Color Values (yDest, xDest)
  1 -> Red
  2 -> Orange
  3 -> Yellow
  4 -> Lime Green
  5 -> Dark Green
  6 -> Cyan
  7 -> Blue
  8 -> Violet
  9 -> Magenta
*/

int xStart[9] = {100, 100, 100, 100, 100, 300, 300, 300, 300};
int yStart[9] = {-100, -350, -625, -875, -1150, -100, -350, -625, -875};
int xDest[9] = {1150, 900, 630, 1150, 900, 630, 1150, 900, 630};
int yDest[9] = {-100, -100, -100, -325, -325, -325, -550, -550, -550};
int destinationIndicie = -1;

// Predefined colors
String predefinedColors[9] = {"red", "yellow", "orange", "magenta",
 "violet", "blue", "cyan", "darkGreen", "limeGreen"};

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pins as outputs.
  // pinMode(ENA_PIN, OUTPUT);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(SOL_PIN, OUTPUT);         // Red
  stepperY.setMaxSpeed(2000);
  stepperX1.setMaxSpeed(2000);
  stepperX2.setMaxSpeed(2000);
  stepperY.setAcceleration(49);
  stepperX1.setAcceleration(49);
  stepperX2.setAcceleration(49);
  limitSwitchY.setDebounceTime(50); // set debounce time to 50 milliseconds
  limitSwitchX1.setDebounceTime(50); // set debounce time to 50 milliseconds
  limitSwitchX2.setDebounceTime(50); // set debounce time to 50 milliseconds
  startUpY = true;
  startUpX1 = true;
  startUpX2 = true;
}

/* 
  Destination Array Indicies to Corresponding Color Values (yDest, xDest)
  1 -> Red
  2 -> Orange
  3 -> Yellow
  4 -> Lime Green
  5 -> Dark Green
  6 -> Cyan
  7 -> Blue
  8 -> Violet
  9 -> Magenta
*/

/*
  Polls color from Rasbperry Pi one time
  @param None
  @return integer corresponding to final grid placement of image (yDest, xDest indicies)
*/

int pollColor() {
  // Check if data is available to read.
  if (Serial.available() > 0) {
    // Read and wait for new data to arrive
    delay(10);
    String receivedColor = Serial.readStringUntil('\n');
    // Loop through the predefined colors array
    for (int i = 0; i < 9; i++) {
      if (receivedColor == predefinedColors[i]) {
        return i; // Match found, return correct indicie
      }
    }
  }
  else {
    Serial.println("No data received.");
    return -1;
  }
}

// the loop function runs over and over again forever
void loop() {
  // On start up I want x1(left, rg on A bb on B) to go counter clockwise(+) and x2(right, rg on A bb on B) to go clockwise(-)
  if(startUpX1 == true || startUpX2 == true)
  {
    startUpX1 = false;
    startUpX2 = false;
    stepperX1.setSpeed(100);
    stepperX2.setSpeed(-100);
    limitSwitchX1.loop();
    limitSwitchX2.loop();
    int stateX1 = limitSwitchX1.getState();
    int stateX2 = limitSwitchX2.getState();
    while(stateX1 == HIGH || stateX2 == HIGH)
    {
      limitSwitchX1.loop();
      limitSwitchX2.loop();
      stepperX1.setSpeed(100);
      stepperX2.setSpeed(-100);
      if(stateX1 == HIGH)
      {
        stepperX1.run();
      }
      if(stateX2 == HIGH)
      {
        stepperX2.run();
      }
      stateX1 = limitSwitchX1.getState();
      stateX2 = limitSwitchX2.getState();
    }
    while(stateX1 == LOW || stateX2 == LOW)
    {
      limitSwitchX1.loop();
      limitSwitchX2.loop();
      stepperX1.setSpeed(-10);
      stepperX2.setSpeed(10);
      if(stateX1 == LOW)
      {
        stepperX1.run();
      }
      if(stateX2 == LOW)
      {
        stepperX2.run();
      }
      stateX1 = limitSwitchX1.getState();
      stateX2 = limitSwitchX2.getState();
    }
    stepperX1.setCurrentPosition(0);
    stepperX2.setCurrentPosition(0);
  }

  if(startUpY == true)
  {
    startUpY = false;
    stepperY.setSpeed(100);
    limitSwitchY.loop();
    int stateY = limitSwitchY.getState();
    while(stateY == HIGH)
    {
      limitSwitchY.loop();
      stepperY.setSpeed(100);
      stepperY.run();
      stateY = limitSwitchY.getState();
    }
    while(stateY == LOW)
    {
      limitSwitchY.loop();
      stepperY.setSpeed(-10);
      stepperY.run();
      stateY = limitSwitchY.getState();
    }
    stepperY.setCurrentPosition(0);
  }

  // This is the old zeroing, the new limit switch zeroing is above
  // stepperY.setCurrentPosition(0);    // Set home
  // stepperX1.setCurrentPosition(0);    // Set home
  // stepperX2.setCurrentPosition(0);    // Set home
  // stepperY.stop();

  // This is the start of the code that should allow us to get multiple peices
  for(int i = 0; i < 9; i++)
  {
    // int xStart[1] = {100}
    // int yStart[1] = {-100}
    // int xDest[1] = {500}
    // int yDest[1] = {-500}


    // Move y to the start
    stepperY.moveTo(yStart[i]);              
    stepperY.runToPosition();
    delay(1000);
    stepperY.stop();

    // Move x to the start
    stepperX1.moveTo(-1*xStart[i]);
    stepperX2.moveTo(xStart[i]); 
    while(stepperX1.distanceToGo() != 0 || stepperX2.distanceToGo() != 0)
    {
      if(stepperX1.distanceToGo() != 0)
      {
        stepperX1.run();
      }
      if(stepperX2.distanceToGo() != 0)
      {
        stepperX2.run();
      }
    }

    // Sanity Check + Grab destination indicie based on color
    if(pollColor() != -1) {
       destinationIndicie = pollColor();
    } else destinationIndicie = -1;

    // extend the actuator
    digitalWrite(IN1_PIN, HIGH);
    digitalWrite(IN2_PIN, LOW);   // actuator will stop extending automatically when reaching the limit
    delay(2000);                  // delay to let the actuator go all the way down before suction
    digitalWrite(SOL_PIN, HIGH);  // Start suction
    delay(4000);                  // Wait for 4 seconds before going up to secure peice

    // retracts the actuator
    digitalWrite(IN1_PIN, LOW);
    digitalWrite(IN2_PIN, HIGH);  // actuator will stop extending automatically when reaching the limit
    delay(5000);                  // Let actuator go all the way up and pause

    // Move with the piece in y direction to the destination
    stepperY.moveTo(yDest[destinationIndicie]);              
    stepperY.runToPosition();
    delay(1000);
    stepperY.stop();

    delay(1000);                  // Delay for debug purposes

    // Move with the piece in x direction to the destination 
    stepperX1.moveTo(-1*xDest[destinationIndicie]);
    stepperX2.moveTo(xDest[destinationIndicie]); 
    while(stepperX1.distanceToGo() != 0 || stepperX2.distanceToGo() != 0)
    {
      if(stepperX1.distanceToGo() != 0)
      {
        stepperX1.run();
      }
      if(stepperX2.distanceToGo() != 0)
      {
        stepperX2.run();
      }
    }

    delay(1000);                  // Delay for debug purposes

    // extend the actuator
    digitalWrite(IN1_PIN, HIGH);
    digitalWrite(IN2_PIN, LOW);
    delay(2000); // actuator will stop extending automatically when reaching the limit

    delay(4000); // Hold the peice for 4 seconds 
    digitalWrite(SOL_PIN, LOW);  // Stop suction, drop piece

    // retracts the actuator
    digitalWrite(IN1_PIN, LOW);
    digitalWrite(IN2_PIN, HIGH);
    delay(5000); // actuator will stop extending automatically when reaching the limit
  }


  // This is the code for getting one peice
  // // extend the actuator
  // digitalWrite(IN1_PIN, HIGH);
  // digitalWrite(IN2_PIN, LOW);   // actuator will stop extending automatically when reaching the limit
  // delay(2000);                  // delay to let the actuator go all the way down before suction
  // digitalWrite(SOL_PIN, HIGH);  // Start suction
  // delay(5000);                  // Wait for 5 seconds before going up to secure peice

  // // retracts the actuator
  // digitalWrite(IN1_PIN, LOW);
  // digitalWrite(IN2_PIN, HIGH);  // actuator will stop extending automatically when reaching the limit
  // delay(6000);                  // Let actuator go all the way up and pause


  // // Move with the piece in y direction
  // stepperY.moveTo(-400);              
  // stepperY.runToPosition();
  // delay(1000);
  // stepperY.stop();

  // delay(2000);                  // Delay for debug purposes

  // // Move with the piece in x direction
  // stepperX1.moveTo(-400);
  // stepperX2.moveTo(400); 
  // while(stepperX1.distanceToGo() != 0 || stepperX2.distanceToGo() != 0)
  // {
  //   if(stepperX1.distanceToGo() != 0)
  //   {
  //     stepperX1.run();
  //   }
  //   if(stepperX2.distanceToGo() != 0)
  //   {
  //     stepperX2.run();
  //   }
  // }

  // delay(2000);                  // Delay for debug purposes

  // // extend the actuator
  // digitalWrite(IN1_PIN, HIGH);
  // digitalWrite(IN2_PIN, LOW);
  // delay(2000); // actuator will stop extending automatically when reaching the limit

  // delay(5000); // Hold the peice for 5 seconds 
  // digitalWrite(SOL_PIN, LOW);  // Stop suction, drop piece

  // // retracts the actuator
  // digitalWrite(IN1_PIN, LOW);
  // digitalWrite(IN2_PIN, HIGH);
  // delay(6000); // actuator will stop extending automatically when reaching the limit


  // Going back home

  // Move back to home without peice in the y direction
  stepperY.moveTo(-100);              
  stepperY.runToPosition();
  delay(1000);
  stepperY.stop();

  delay(2000);                  // Delay for debug purposes

  // Move back to home without the peice in the x direction
  stepperX1.moveTo(-100);
  stepperX2.moveTo(100); 
  while(stepperX1.distanceToGo() != 0 || stepperX2.distanceToGo() != 0)
  {
    if(stepperX1.distanceToGo() != 0)
    {
      stepperX1.run();
    }
    if(stepperX2.distanceToGo() != 0)
    {
      stepperX2.run();
    }
  }

  delay(10000); // actuator will stop retracting automatically when reaching the limit
}
