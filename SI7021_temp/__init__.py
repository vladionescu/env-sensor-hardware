#!/usr/bin/env python
# Modified by Vlad Ionescu (github.com/vladionescu)
#
# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# SI7021
# This code is designed to work with the SI7021_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Humidity?sku=SI7021_I2CS#tabs-0-product_tabset-2

import smbus
import time

class SI7021_temp(object):
  def __init__(self, address=0x40):
    # Get I2C bus
    self.bus = smbus.SMBus(1)

    # 0x40(64)	SI7021 address (default)
    self.ADDRESS = address

  def humidity(self):
    # 0xF5(245)	Select Relative Humidity NO HOLD master mode
    self.bus.write_byte(self.ADDRESS, 0xF5)

    time.sleep(0.3)

    # Read data back, 2 bytes, Humidity MSB first
    data0 = self.bus.read_byte(self.ADDRESS)
    data1 = self.bus.read_byte(self.ADDRESS)

    # Convert the data
    humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6

    return humidity

  def tempC(self):
    # Get the raw bytes
    data0, data1 = self.raw_temp()

    # Convert the raw data
    cTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
    
    return cTemp

  def tempF(self):
    # Convert celsius to farenheit
    return self.tempC() * 1.8 + 32

  def raw_temp(self):
    # 0xF3(243)	Select Temperature NO HOLD master mode
    self.bus.write_byte(self.ADDRESS, 0xF3)

    time.sleep(0.3)

    # Read data back, 2 bytes, Temperature MSB first
    data0 = self.bus.read_byte(self.ADDRESS)
    data1 = self.bus.read_byte(self.ADDRESS)

    return (data0, data1)
