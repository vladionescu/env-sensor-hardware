#!/usr/bin/python
#import RS0010_screen # use when running outside RS0010_screen dir
from __init__ import RS0010_screen # use when running within RS0010_screen dir
import time

def main():
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

  while True:
    screen.line1("They don't think")
    screen.line2("it be like it is")

    time.sleep(5)

    screen.line1("but it do.")
    screen.line2("-Oscar Gamble")

    time.sleep(5)

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    RS0010_screen.gpio_cleanup()
