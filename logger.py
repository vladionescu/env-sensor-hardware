#!/usr/bin/env python3
# Vlad Ionescu (github.com/vladionescu) 2016

from RS0010_screen import RS0010_screen
from SI7021_temp import SI7021_temp
from TSL2561 import TSL2561
import argparse, time

def main():
  # Setup screen
  # Define GPIO to LCD pin mapping
  LCD_RS = 21
  LCD_E  = 20
  LCD_D4 = 6
  LCD_D5 = 26
  LCD_D6 = 19
  LCD_D7 = 13

  screen = RS0010_screen(RS=LCD_RS, E=LCD_E, D4=LCD_D4,
    D5=LCD_D5, D6=LCD_D6, D7=LCD_D7)

  screen.clear()

  # Setup temp sensor
  temp = SI7021_temp()

  # Setup luminosity sensor

  # Try to get the TSL twice with a 2 sec wait
  # If the sensor doesn't respond, make the getLux()
  #   method return ERR! instead.
  for i in range(2):
    light = TSL2561(bus=1)
    if light.foundSensor():
      # If the sensor responds, set it up and continue
      light.setGain(light.GAIN_16X)
      light.setTiming(light.INTEGRATIONTIME_13MS)
      break
    time.sleep(2)
  else:
    def fakeLux():
      return "ERR!"
    light.getLux = fakeLux
	

  while True:
    farenheit = temp.tempF()
    relative_humidity = temp.humidity()
    lux = light.getLux()

    the_time = time.strftime("%a  %H:%M:%S")

    screen.line1( "{:.1f} F  {:.1f}%RH".
      format(temp.tempF(), temp.humidity()),
      justify="center" )
  # screen.line2( "{} Lux {}".
  #   format(the_time, light.getLux()) )
    screen.line2( the_time, justify="center" )

    time.sleep(3)

    screen.line1( "Lux {}".format(light.getLux()),
      justify="center" )

    time.sleep(3)

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    RS0010_screen.close(True)
