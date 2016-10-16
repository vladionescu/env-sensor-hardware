#!/usr/bin/python
# RS0010_screen package by Vlad Ionescu (github.com/vladionescu) is based on:
#   lcd_16x2.py by Matt Hawkins (http://www.raspberrypi-spy.co.uk/)
#
# Copyright 2015 Matt Hawkins
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)	     - GROUND
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V	     - NOT USED
# 16: LCD Backlight GND	     - NOT USED

import RPi.GPIO as GPIO
import time

class RS0010_screen(object):
  # Maximum characters per line
  LCD_WIDTH = 16

  # LCD RAM addresses for each line
  LCD_LINE_1 = 0x80
  LCD_LINE_2 = 0xC0

  # Timing constants
  E_PULSE = 0.0005
  E_DELAY = 0.0005

  # Operation type when sending data to LCD
  LCD_CHR = True
  LCD_CMD = False

  def __init__(self, RS, E, D4, D5, D6, D7,
    LCD_WIDTH=None, LINE_1_REGISTER=None, LINE_2_REGISTER=None,
    E_PULSE=None, E_DELAY=None):

    self.LCD_RS = RS
    self.LCD_E = E
    self.LCD_D4 = D4
    self.LCD_D5 = D5
    self.LCD_D6 = D6
    self.LCD_D7 = D7

    if LCD_WIDTH is not None:
      self.LCD_WIDTH = LCD_WIDTH

    if LINE_1_REGISTER is not None:
      self.LCD_LINE_1 = LINE_1_REGISTER

    if LINE_2_REGISTER is not None:
      self.LCD_LINE_2 = LINE_2_REGISTER

    if E_PULSE is not None:
      self.E_PULSE = float(E_PULSE)

    if E_DELAY is not None:
      self.E_DELAY = float(E_DELAY)

    # Set the RPi pins connected to the LCD to output
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
    GPIO.setup(self.LCD_E, GPIO.OUT)  # E
    GPIO.setup(self.LCD_RS, GPIO.OUT) # RS
    GPIO.setup(self.LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(self.LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(self.LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(self.LCD_D7, GPIO.OUT) # DB7

    # Initialise display
    self.lcd_byte(0x33, self.LCD_CMD) # 110011 Initialise
    self.lcd_byte(0x32, self.LCD_CMD) # 110010 Initialise
    self.lcd_byte(0x06, self.LCD_CMD) # 000110 Cursor move direction
    self.lcd_byte(0x0C, self.LCD_CMD) # 001100 Display On, Cursor Off, Blink Off
    self.lcd_byte(0x28, self.LCD_CMD) # 101000 Data length, number of lines, font size

    self.clear()
    time.sleep(self.E_DELAY)

  def clear(self):
    self.lcd_byte(0x01, self.LCD_CMD) # 000001 Clear display

  @staticmethod
  def gpio_cleanup():
    GPIO.cleanup()

  def lcd_byte(self, bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command

    GPIO.output(self.LCD_RS, mode) # RS

    # High bits
    GPIO.output(self.LCD_D4, False)
    GPIO.output(self.LCD_D5, False)
    GPIO.output(self.LCD_D6, False)
    GPIO.output(self.LCD_D7, False)
    if bits&0x10==0x10:
      GPIO.output(self.LCD_D4, True)
    if bits&0x20==0x20:
      GPIO.output(self.LCD_D5, True)
    if bits&0x40==0x40:
      GPIO.output(self.LCD_D6, True)
    if bits&0x80==0x80:
      GPIO.output(self.LCD_D7, True)

    # Toggle 'Enable' pin
    self.lcd_toggle_enable()

    # Low bits
    GPIO.output(self.LCD_D4, False)
    GPIO.output(self.LCD_D5, False)
    GPIO.output(self.LCD_D6, False)
    GPIO.output(self.LCD_D7, False)
    if bits&0x01==0x01:
      GPIO.output(self.LCD_D4, True)
    if bits&0x02==0x02:
      GPIO.output(self.LCD_D5, True)
    if bits&0x04==0x04:
      GPIO.output(self.LCD_D6, True)
    if bits&0x08==0x08:
      GPIO.output(self.LCD_D7, True)

    # Toggle 'Enable' pin
    self.lcd_toggle_enable()

  def lcd_toggle_enable(self):
    # Toggle enable
    time.sleep(self.E_DELAY)
    GPIO.output(self.LCD_E, True)
    time.sleep(self.E_PULSE)
    GPIO.output(self.LCD_E, False)
    time.sleep(self.E_DELAY)

  def lcd_string(self, message, line):
    # Send string to display
    message = message.ljust(self.LCD_WIDTH," ")

    self.lcd_byte(line, self.LCD_CMD)

    for i in range(self.LCD_WIDTH):
      self.lcd_byte(ord(message[i]),self.LCD_CHR)

  def line1(self, message=""):
    self.lcd_string(message, self.LCD_LINE_1)

  def line2(self, message=""):
    self.lcd_string(message, self.LCD_LINE_2)

  def close(self, clear=False):
    if clear:
      self.clear()

    GPIO.cleanup()
