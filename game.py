#include <FastLED.h> // Inclusie van de FastLED-bibliotheek
#include <TM1637Display.h> // Inclusie van de TM1637-displaybibliotheek
#define NUM_LEDS 60   // Aantal LED's op de strip
#define LED_PIN 5    // Pin voor de LED-strip
#define CLK_PIN 2    // Pin voor de TM1637 CLK
#define DIO_PIN 3    // Pin voor de TM1637 DIO
#define RESET_PIN 4  // Pin voor de resetknop
CRGB leds[NUM_LEDS]; // Array voor LED-kleuren

const int sensorPins[] = {9, 10, 11, 12, 13}; // Pinnummers voor de sensoren
const int numSensors = sizeof(sensorPins) / sizeof(sensorPins[0]); // Aantal sensoren

int blikjeStatus[] = {LOW, LOW, LOW, LOW, LOW}; // Status van de blikjes bij elke sensor
CRGB sensorColors[] = {CRGB::Blue, CRGB::Red, CRGB::Green, CRGB::Yellow, CRGB::Orange}; // Kleuren voor elke sensor

int verwijderdeBlikjes = 0; // Variabele om het aantal verwijderde blikjes bij te houden

TM1637Display display(CLK_PIN, DIO_PIN); // TM1637-display

void setup() {
  Serial.begin(9600); // Initialiseer de seriële communicatie
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS); // Configuratie van LED-strip
  for (int i = 0; i < numSensors; i++) {
    pinMode(sensorPins[i], INPUT); // Zet de sensorpinnen als invoer
  }
  pinMode(RESET_PIN, INPUT_PULLUP); // Zet de resetpin als invoer met pull-up weerstand
  display.setBrightness(0x0a); // Stel helderheid van het display in (0x00 tot 0x0f)
  display.clear(); // Wis het display
  // Initialisatie van de LED-strip
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Purple; // Uitschakelen van alle LED's
  }
  FastLED.show(); // Toon de wijzigingen op de LED-strip
}

void loop() {
  // Controleer of de resetknop is ingedrukt
  if (digitalRead(RESET_PIN) == LOW) {
    resetGame(); // Roep de resetGame-functie aan als de knop is ingedrukt
    // LEDs blauw laten gaan over 5 stappen
    for (int i = 0; i < NUM_LEDS; i += 5) {
      for (int j = i; j < i + 5; j++) {
        leds[j] = CRGB::Blue;
      }
      FastLED.show();
      delay(100);
      // Schakel de LEDs uit na elke 5 stappen
      for (int j = i; j < i + 5; j++) {
        leds[j] = CRGB::Black;
      }
    }
  }

  // Lees de status van elke sensor en update de status van de blikjes
  for (int i = 0; i < numSensors; i++) {
    int sensorStatus = digitalRead(sensorPins[i]);
    if (sensorStatus != blikjeStatus[i]) {
      if (sensorStatus == LOW) {
        Serial.print("Blikje geplaatst bij sensor ");
        Serial.println(i + 1);
      } else {
        Serial.print("Blikje verwijderd bij sensor ");
        Serial.println(i + 1);
        // Laat de LED-strip snel rood flikkeren
        flickerRed();
        // Verhoog het aantal verwijderde blikjes
        verwijderdeBlikjes++;
        Serial.print("Totaal aantal verwijderde blikjes: ");
        Serial.println(verwijderdeBlikjes);
        
        // Controleer of het aantal verwijderde blikjes 5 of minder is
        if (verwijderdeBlikjes <= 5) {
          display.showNumberDec(verwijderdeBlikjes, false, 4, 0); // Toon het aantal verwijderde blikjes op het display
        } else {
          // Reset de game als het aantal verwijderde blikjes meer dan 5 is
          resetGame();
        }
      }
      blikjeStatus[i] = sensorStatus;
    }
  }

  // Vertraging om de loop langzamer te laten lopen voor betere leesbaarheid
  delay(100); // Wacht 100 milliseconden voordat de lus opnieuw wordt uitgevoerd
}

// Functie om de LED-strip snel rood te laten flikkeren
void flickerRed() {
  for (int i = 0; i < 3; i++) { // 3 keer flikkeren
    // LED's rood maken
    for (int j = 0; j < NUM_LEDS; j++) {
      leds[j] = CRGB::Red;
    }
    FastLED.show();
    delay(100); // Flikkersnelheid
    // LED's uitschakelen
    for (int j = 0; j < NUM_LEDS; j++) {
      leds[j] = CRGB::Purple;
    }
    FastLED.show();
    delay(100); // Pauze tussen flikkeringen
  }
}

// Functie om de game te resetten
void resetGame() {
  verwijderdeBlikjes = 0; // Reset het aantal verwijderde blikjes
  display.clear(); // Wis het display
  // Schakel alle LED's uit op de LED-strip
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Purple;
  }
  FastLED.show(); // Toon de wijzigingen op de LED-strip
}
