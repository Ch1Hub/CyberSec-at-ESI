#include <Arduino.h>
#include <Keypad.h>

const byte ROW_NUM    = 4;    // four rows
const byte COLUMN_NUM = 3;    // three columns

char keys[ROW_NUM][COLUMN_NUM] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'*','0','#'}
};

byte pin_rows[ROW_NUM] = {9, 8, 7, 6};  // Connect to the row pinouts of the keypad
byte pin_column[COLUMN_NUM] = {5, 4, 3};  // Connect to the column pinouts of the keypad

Keypad keypad = Keypad(makeKeymap(keys), pin_rows, pin_column, ROW_NUM, COLUMN_NUM);

void setup() {
  Serial.begin(9600);
}

void loop() {
  char key = keypad.getKey();  // Get the key pressed

  if (key) {
    Serial.println(key);  // Print the key to the serial monitor
  }
}
