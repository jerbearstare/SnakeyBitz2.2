const byte coinSig = 2; // analog pin on board
const int ledpin = LED_BUILTIN;
bool previousCoinSignal = false;
const float coinValue = 0.25;
float bankValue = 0.00;

//This is a setup function that includes several lines of code that set up the program to run. The Seial.begin function sets the baud rate for serial communication. The pi nMode function sets the pins in the board to input or output. The digita lRead function reads the coin signal. The Seri al.print function prints "coinReader1.4" to the serial port. 

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(ledpin, OUTPUT);
  pinMode(coinSig, INPUT_PULLUP);      
  Serial.print(bankValue);            
  previousCoinSignal = digitalRead(coinSig); 
}

// Function for Led
void led(){
  digitalWrite(ledpin, HIGH);
  delay(100);
  digitalWrite(ledpin, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  byte currentCoinSignal = digitalRead(coinSig);
  if(currentCoinSignal != previousCoinSignal) {
    // Save the state for the next iteration
    previousCoinSignal = currentCoinSignal;
    digitalWrite(ledpin, HIGH);
    if (currentCoinSignal == HIGH){
      bankValue = bankValue + coinValue;
      led(); 
      Serial.println(bankValue);
      }       
    }  
 }