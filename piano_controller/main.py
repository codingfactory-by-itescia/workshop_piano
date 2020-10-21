import wiringpi

wiringpi.wiringPiSetup()

wiringpi.pinMode(7, 1)

wiringpi.digitalWrite(7, 1)