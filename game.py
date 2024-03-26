#include <Adafruit_NeoPixel.h>
#include <FastLED.h>
#include <TM1637Display.h>
#include <Servo.h>

// Definities en parameters voor NeoPixel-strip
#define PIN            53
#define PIN2           52
#define PIN3           51
#define PIN4           50
#define PIN5           49

#define NUMPIXELS       30
#define NUMPIXELS2      30
#define NUMPIXELS3      30
#define NUMPIXELS4      30
#define NUMPIXELS5      30

#define brightnessValue 50

// Definities en parameters voor FastLED-strip
#define NUM_LEDS 300
#define LED_PIN 45
#define RESET_PIN 47
#define SERVO_PIN A0
#define SERVO_PIN2 A1

// Definities en parameters voor TM1637-display
#define CLK_PIN 2
#define DIO_PIN 3

#define RELAY_PIN 22

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels2 = Adafruit_NeoPixel(NUMPIXELS2, PIN2, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels3 = Adafruit_NeoPixel(NUMPIXELS3, PIN3, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels4 = Adafruit_NeoPixel(NUMPIXELS4, PIN4, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels5 = Adafruit_NeoPixel(NUMPIXELS5, PIN5, NEO_GRB + NEO_KHZ800);

CRGB leds[NUM_LEDS];
TM1637Display display(CLK_PIN, DIO_PIN);
Servo resetServo;
Servo resetServo2;

const int sensorPins[] = {8, 9, 10, 11, 12};
const int numSensors = sizeof(sensorPins) / sizeof(sensorPins[0]);
int blikjeStatus[] = {LOW, LOW, LOW, LOW, LOW};
CRGB sensorColors[] = {CRGB::Blue, CRGB::Red, CRGB::Green, CRGB::Yellow, CRGB::Orange};
int verwijderdeBlikjes = 0;

void setup() {
    Serial.begin(9600);
    pixels.show();
    pixels2.show();
    pixels3.show();
    pixels4.show();    
    pixels5.show();
    pixels.begin();
    pixels.setBrightness(brightnessValue);
    pixels2.begin();
    pixels2.setBrightness(brightnessValue);
    pixels3.begin();
    pixels3.setBrightness(brightnessValue);
    pixels4.begin();
    pixels4.setBrightness(brightnessValue);
    pixels5.begin();
    pixels5.setBrightness(brightnessValue);
        // Zet alle NeoPixel-dots uit
    for (int i = 0; i < NUMPIXELS; i++) {
        pixels.setPixelColor(i, pixels.Color(0, 0, 0)); 
        pixels2.setPixelColor(i, pixels2.Color(0, 0, 0)); 
        pixels3.setPixelColor(i, pixels3.Color(0, 0, 0)); 
        pixels4.setPixelColor(i, pixels4.Color(0, 0, 0)); 
        pixels5.setPixelColor(i, pixels5.Color(0, 0, 0)); 
    }
    
    FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);

    pinMode(RELAY_PIN, OUTPUT);

    for (int i = 0; i < numSensors; i++) {
        pinMode(sensorPins[i], INPUT);
    }
    pinMode(RESET_PIN, INPUT_PULLUP);

    resetServo.attach(SERVO_PIN);
    resetServo2.attach(SERVO_PIN2);

    display.setBrightness(0x0a);
    display.clear();

    for (int i = 0; i < NUM_LEDS; i++) {
        leds[i] = CRGB::Purple;
    }
    FastLED.show();
    resetServo.write(0);
    resetServo2.write(0);
  resetGame();

}

void loop() {
    if (digitalRead(RESET_PIN) == LOW) {
        resetGame();
    }

    for (int i = 0; i < numSensors; i++) {
        int sensorStatus = digitalRead(sensorPins[i]);
        if (sensorStatus != blikjeStatus[i]) {
            if (sensorStatus == HIGH) {
                Serial.print("Blikje verwijderd bij sensor");
                Serial.println(i + 1);
            } else {
                Serial.print("Blikje geplaatst bij sensor");
                Serial.println(i + 1);
                flickerRed();
                verwijderdeBlikjes++;
                Serial.print("Totaal aantal geplaatst blikjes: ");
                Serial.println(verwijderdeBlikjes);
                if (verwijderdeBlikjes <= 5) {
                    handlePoint(verwijderdeBlikjes);
                } else {
                    for (int i = 0; i < NUM_LEDS; i++) {
                        leds[i] = CRGB::Red;
                    }
                    FastLED.show();
                }
            }
            blikjeStatus[i] = sensorStatus;
        }
    }
    delay(100);
}

void flickerRed() {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < NUM_LEDS; j++) {
            leds[j] = CRGB::Red;
        }
        FastLED.show();
        delay(100);

        for (int j = 0; j < NUM_LEDS; j++) {
            leds[j] = CRGB::Purple;
        }
        FastLED.show();
        delay(100);
    }
}

void resetGame() {
    verwijderdeBlikjes = 0;
    display.clear();

    // Zet alle NeoPixel-dots uit
    for (int i = 0; i < NUMPIXELS; i++) {
        pixels.setPixelColor(i, pixels.Color(0, 0, 0)); 
        pixels2.setPixelColor(i, pixels2.Color(0, 0, 0)); 
        pixels3.setPixelColor(i, pixels3.Color(0, 0, 0)); 
        pixels4.setPixelColor(i, pixels4.Color(0, 0, 0)); 
        pixels5.setPixelColor(i, pixels5.Color(0, 0, 0)); 
    }
    pixels.show();
    pixels2.show();
    pixels3.show();
    pixels4.show();    
    pixels5.show();

    for (int i = 0; i < NUM_LEDS; i++) {
        leds[i] = CRGB::Red;
    }
    FastLED.show();
    digitalWrite(RELAY_PIN, HIGH);
    delay(2000);

    resetServo.write(90);
    resetServo2.write(90);
    delay(2000);

    verwijderdeBlikjes = 0;
    display.clear();

    resetServo.write(0);
    resetServo2.write(0);
    delay(2000);
    digitalWrite(RELAY_PIN, LOW);
    delay(2000);

    for (int i = 0; i < NUM_LEDS; i++) {
        leds[i] = CRGB::Green;
    }
    FastLED.show();
}

void handlePoint(int point) {
    // Converteer het punt naar de juiste TM1637-displayweergave
    // bijvoorbeeld, voor punt 1 toon "1" op de display
    display.showNumberDec(point, false);


    switch (point) {
        case 1:
            for (int k = 0; k < NUMPIXELS; k++) {
                pixels.setPixelColor(k, pixels.Color(255, 0, 255)); // Paars
            }
            pixels.show();
            break;
        case 2:
            for (int k = 0; k < NUMPIXELS; k++) {
                pixels2.setPixelColor(k, pixels2.Color(255, 0, 255)); // Paars
            }
            pixels2.show();
            break;
        case 3:
            for (int k = 0; k < NUMPIXELS; k++) {
                pixels3.setPixelColor(k, pixels3.Color(255, 0, 255)); // Paars
            }
            pixels3.show();
            break;
        case 4:
            for (int k = 0; k < NUMPIXELS; k++) {
                pixels4.setPixelColor(k, pixels4.Color(255, 0, 255)); // Paars
            }
            pixels4.show();
            break;
        case 5:
            for (int k = 0; k < NUMPIXELS; k++) {
                pixels5.setPixelColor(k, pixels5.Color(255, 0, 255)); // Paars
            }
            pixels5.show();
            break;
        default:
            // Geen actie nodig
            break;
    }
}


