import wiringpi2

wiringpi2.wiringPiSetup()

wiringpi2.pinMode(7, 1)

wiringpi2.digitalWrite(7, 1)