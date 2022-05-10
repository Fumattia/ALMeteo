#include <WiFiManager.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WifiLocation.h>
#include "DHT.h"

#define DHTPIN 4     // what digital pin the DHT22 is conected to
#define DHTTYPE DHT22   // there are multiple kinds of DHT sensors

#define TRIGGER_PIN 0



const char* googleApiKey = "AIzaSyCT51ZUm-Z8nGJkwv-DGv09tbKjwsgZPAQ";
WifiLocation location(googleApiKey);
location_t loc = location.getGeoFromWiFi();

DHT dht(DHTPIN, DHTTYPE);

float temp;
float hum;
int pres = 23;
int qaria = 34;
int pioggia = 1;

String sendtemp, sendhum, sendpres, sendqaria, sendpioggia, sendlat, sendlon, postData;
String tabella = "Prova";

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
  

  Serial.println("Location request data");
  Serial.println(location.getSurroundingWiFiJson());
  Serial.println("Latitude: " + String(loc.lat, 7));
  Serial.println("Longitude: " + String(loc.lon, 7));
  Serial.println("Accuracy: " + String(loc.accuracy));

  // setup temporizzazioni
  tempo=millis();
  lettura_dati=millis()-600000;

  // setup sensori
  dht.begin();

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
  hum = dht.readHumidity();
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
  sendhum = String(hum); 
  sendpres = String(pres); 
  sendqaria = String(qaria); 
  sendpioggia = String(pioggia);

  sendlat = String(loc.lat, 7);
  sendlon = String(loc.lon, 7);
  
   
  return postData = "tabella=" + tabella + "&sendtemp=" + sendtemp + "&sendhum=" + sendhum + "&sendpres=" + sendpres + "&sendqaria=" + sendqaria + "&sendpioggia=" + sendpioggia;
}


void loop() {
  if(wm_nonblocking) wm.process(); // avoid delays() in loop when non-blocking and other long running code  
  checkButton();
  // put your main code here, to run repeatedly:
  tempo=millis();
  if (tempo>lettura_dati+600000)
  { 
    sensori();
    String dati = misurazioni();
    post_data(dati);
    lettura_dati=millis();
  }
}
