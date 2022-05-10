#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// Update HOST URL here

#define HOST "fumacasa.duckdns.org"          // Enter HOST URL without "http:// "  and "/" at the end of URL

#define WIFI_SSID "Saletta"            // WIFI SSID here                                   
#define WIFI_PASSWORD "Casa17fuma"        // WIFI password here

// Declare global variables which will be uploaded to server

int temp = 1;
int hum = 99;
int pres = 23;
int qaria = 34;
int pioggia = 1;

String sendtemp, sendhum, sendpres, sendqaria, sendpioggia, postData;
String tabella = "Prova";


void setup() {
  
       
  Serial.begin(9600);
  Serial.println("Communication Started \n\n");  
  delay(1000);
    
  
  pinMode(LED_BUILTIN, OUTPUT);     // initialize built in led on the board
   
  
  
  WiFi.mode(WIFI_STA);           
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);                                     //try to connect with wifi
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);
  while (WiFi.status() != WL_CONNECTED) 
  { Serial.print(".");
      delay(500); }
  
  Serial.println();
  Serial.print("Connected to ");
  Serial.println(WIFI_SSID);
  Serial.print("IP Address is : ");
  Serial.println(WiFi.localIP());    //print local IP address





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

void loop() { 


  // Convert integer variables to string
  sendtemp = String(temp);  
  sendhum = String(hum); 
  sendpres = String(pres); 
  sendqaria = String(qaria); 
  sendpioggia = String(pioggia);   
  
   
  postData = "tabella=" + tabella + "&sendtemp=" + sendtemp + "&sendhum=" + sendhum + "&sendpres=" + sendpres + "&sendqaria=" + sendqaria + "&sendpioggia=" + sendpioggia;
  
  // We can post values to PHP files as  example.com/dbwrite.php?name1=val1&name2=val2&name3=val3
  // Hence created variable postDAta and stored our variables in it in desired format
  // For more detials, refer:- https://www.tutorialspoint.com/php/php_get_post.htm
  
  // Update Host URL here:-  
  delay(5000);
  
    
  post_data(postData);
  delay(600000);

  
  
  // if connection eatablished then do this
  //if (httpCode == 200) { 
  //  Serial.println("Values uploaded successfully."); 
  //  Serial.println(httpCode); 
  //String webpage = http.getString();    // Get html webpage output and store it in a string
  //Serial.println(webpage + "\n"); 
  //}
  
  // if failed to connect then return and restart
  
  //else { 
  //  Serial.println(httpCode); 
  //  Serial.println("Failed to upload values. \n"); 
  //  http.end(); 
  //  return; }
  
    


}
