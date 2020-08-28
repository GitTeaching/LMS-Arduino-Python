//#include <LiquidCrystal.h>
#include <dht.h>

//LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
dht DHT;
#define DHT11_PIN 7


void setup(){
  //lcd.begin(16, 2);
  Serial.begin(9600);
}

void loop(){
  
  int chk = DHT.read11(DHT11_PIN);

  Serial.print(DHT.temperature);
  Serial.print(' ');
  Serial.println(DHT.humidity);
  delay(2000);
  
  // Wiith LCD version 
  //lcd.setCursor(0,0); 
  //lcd.print("Temp: ");
  //lcd.print(DHT.temperature);
  //lcd.print((char)223);
  //lcd.print("C");
  //lcd.setCursor(0,1);
  //lcd.print("Humidity: ");
  //lcd.print(DHT.humidity);
  //lcd.print("%");
  
  
}
