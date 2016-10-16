#!/usr/bin/env python
#import SI7021_temp # use outside of package dir dir
from __init__ import SI7021_temp # use inside the package dir

def main():
  temp = SI7021_temp()

  # Output data to screen
  print "Relative Humidity is : %.2f %%" % temp.humidity()
  print "Temperature in Celsius is : %.2f C" % temp.tempC()
  print "Temperature in Fahrenheit is : %.2f F" % temp.tempF()

if __name__ == '__main__':
  main()
