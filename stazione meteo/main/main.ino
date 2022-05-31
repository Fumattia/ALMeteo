#include <WiFiManager.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include "DHT.h"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

#define DHTPIN 14     // what digital pin the DHT22 is conected to

#define mq2 12     // what digital pin the mq2 is conected to
#define DHTTYPE DHT22   // there are multiple kinds of DHT sensors

#define TRIGGER_PIN 0
#define SEALEVELPRESSURE_HPA (1022.25)

Adafruit_BMP280 bme; // I2C



DHT dht(DHTPIN, DHTTYPE);

float temp;
float temp2;
float hum;
float perc;
float pres;
float alt;
float qaria;
int pioggia = 1;

String sendtemp, sendtemp2, sendhum, sendperc, sendpres, sendalt, sendqaria, sendpioggia, sendlat, sendlon, postData;
String tabella = "Dati";
String sendcodice = "Stazione_2";

unsigned long tempo;
unsigned long lettura_dati;

// wifimanager can run in a blocking mode or a non blocking mode
// Be sure to know how to process loops with no delay() if using non blocking
bool wm_nonblocking = false; // change to true to use non blocking

WiFiManager wm; // global wm instance
WiFiManagerParameter custom_field; // global param ( for non blocking w params )

void setup() {
  WiFi.mode(WIFI_STA); // explicitly set mode, esp defaults to STA+AP  
  Serial.begin(9600);
  Serial.setDebugOutput(true);  
  delay(3000);
  Serial.println("\n Starting");

  pinMode(TRIGGER_PIN, INPUT);
  
  // wm.resetSettings(); // wipe settings

  if(wm_nonblocking) wm.setConfigPortalBlocking(false);

  // add a custom input field
  int customFieldLength = 40;
  const char* custom_radio_str = "<br/><label for='customfieldid'>Custom Field Label</label><input type='radio' name='customfieldid' value='1' checked> One<br><input type='radio' name='customfieldid' value='2'> Two<br><input type='radio' name='customfieldid' value='3'> Three";
  new (&custom_field) WiFiManagerParameter(custom_radio_str); // custom html input
  wm.addParameter(&custom_field);
  wm.setSaveParamsCallback(saveParamCallback);
  std::vector<const char *> menu = {"wifi","info","param","sep","restart","exit"};
  wm.setMenu(menu);
  
  bool res;
  res = wm.autoConnect("ALMeteo",""); // password protected ap

  if(!res) {
    Serial.println("Failed to connect or hit timeout");
    // ESP.restart();
  } 
  else {
    //if you get here you have connected to the WiFi    
    Serial.println("connected...yeey :)");
  }
  // setup location
 

  // setup temporizzazioni
  tempo=millis();
  lettura_dati=millis()-300000;

  // setup sensori
  dht.begin();
  pinMode(mq2, INPUT);
  bool status;
  // default settings
  // (you can also pass in a Wire library object like &Wire2)
  status = bme.begin(0x76);  
  if (!status) {
    Serial.println("Could not find a valid BMP280 sensor, check wiring!");
    while (1);
  }

  Serial.println("Device Started");
  Serial.println("-------------------------------------");
  Serial.println("Running Sensors!");
  Serial.println("-------------------------------------");
}

void checkButton(){
  // check for button press
  if ( digitalRead(TRIGGER_PIN) == LOW ) {
    // poor mans debounce/press-hold, code not ideal for production
    delay(50);
    if( digitalRead(TRIGGER_PIN) == LOW ){
      Serial.println("Button Pressed");
      // still holding button for 3000 ms, reset settings, code not ideaa for production
      delay(3000); // reset delay hold
      if( digitalRead(TRIGGER_PIN) == LOW ){
        Serial.println("Button Held");
        Serial.println("Erasing Config, restarting");
        wm.resetSettings();
        ESP.restart();
      }
      
      // start portal w delay
      Serial.println("Starting config portal");
      wm.setConfigPortalTimeout(120);
      
      if (!wm.startConfigPortal("OnDemandAP","password")) {
        Serial.println("failed to connect or hit timeout");
        delay(3000);
        // ESP.restart();
      } else {
        //if you get here you have connected to the WiFi
        Serial.println("connected...yeey :)");
      }
    }
  }
}


String getParam(String name){
  //read parameter from server, for customhmtl input
  String value;
  if(wm.server->hasArg(name)) {
    value = wm.server->arg(name);
  }
  return value;
}

void saveParamCallback(){
  Serial.println("[CALLBACK] saveParamCallback fired");
  Serial.println("PARAM customfieldid = " + getParam("customfieldid"));
}

void post_data(String data)
{
  HTTPClient http;    // http object of clas HTTPClient
  WiFiClient wclient; // wclient object of clas HTTPClient    
  
    
  http.begin(wclient, "http://fumacasa.duckdns.org/dbwrite.php");              // Connect to host where MySQL databse is hosted
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");            //Specify content-type header
  int httpCode = http.POST(postData);   // Send POST request to php file and store server response code in variable named httpCode
  Serial.println("Valori mandati");
  http.end();
  Serial.println("Connessione chiusa");
}

void sensori()
{
  temp = dht.readTemperature();
  temp2 = bme.readTemperature();
  hum = dht.readHumidity();
  perc = dht.computeHeatIndex(temp, hum, false);
  pres = bme.readPressure()/100.0F;
  alt = bme.readAltitude(SEALEVELPRESSURE_HPA);
  qaria = analogRead(mq2);
  if (isnan(hum) || isnan(temp)) {
      Serial.println("Failed to read from DHT sensor!");
      temp = NULL;
      hum = NULL;
  }
  if (temp==0 || hum==0)
  {
    sensori();
  }
     
  // perc = dht.computeHeatIndex(temp, hum);
}
String misurazioni()
{
  sendtemp = String(temp);  
  sendtemp2 = String(temp2);  
  sendhum = String(hum); 
  sendperc = String(perc);
  sendpres = String(pres); 
  sendalt = String(alt);  
  sendqaria = String(qaria); 
  sendpioggia = String(pioggia);
  
   
  return postData = "tabella=" + tabella + "&sendtemp=" + sendtemp + "&sendtemp2=" + sendtemp2 + "&sendhum=" + sendhum + "&sendperc=" + sendperc + "&sendpres=" + sendpres + "&sendalt=" + sendalt + "&sendqaria=" + sendqaria + "&sendpioggia=" + sendpioggia + "&sendcodice=" + sendcodice;
}


void loop() {
  if(wm_nonblocking) wm.process(); // avoid delays() in loop when non-blocking and other long running code  
  checkButton();
  // put your main code here, to run repeatedly:
  tempo=millis();
  if (tempo>lettura_dati+300000)
  { 
    sensori();
    String dati = misurazioni();
    post_data(dati);
    lettura_dati=millis();
  }
}
