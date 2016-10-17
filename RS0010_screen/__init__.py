#!/usr/bin/python
# RS0010_screen package by Vlad Ionescu (github.com/vladionescu) is based on:
#   lcd_16x2.py by Matt Hawkins (http://www.raspberrypi-spy.co.uk/)
# With improvements by Robert Coward/Paul Carpenter
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

  # Operation type when sending data to LCD
  LCD_CHR = True
  LCD_CMD = False

  # Timing constants for low level write operations
  # NOTE: Enable cycle time must be at least 1 microsecond
  # NOTE2: These can be zero and the LCD will typically still work OK
  EDEL_TAS =  0.00001      # Address setup time (TAS)
  EDEL_PWEH = 0.00001      # Pulse width of enable (PWEH)
  EDEL_TAH =  0.00001      # Address hold time (TAH)

  # Timing constraints for initialisation steps
  # NOTE: that post clear display must be at least 6.2ms for OLEDs, as opposed
  #  to only 1.4ms for HD44780 LCDs. This has caused confusion in the past.
  #  Setting it to 10ms here to be safe.
  DEL_INITMID = 0.01       # middle of initial write (min 4.1ms)
  DEL_INITNEXT = 0.0002    # post second initial write (min 100ns)
  DEL_POSTCLEAR = 0.01     # post clear display step (busy, min 6.2ms)

  def __init__(self, RS, E, D4, D5, D6, D7,
    LCD_WIDTH=None, LINE_1_REGISTER=None, LINE_2_REGISTER=None):

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

    GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers

    # setup all output pins for driving LCD display
    GPIO.setup(self.LCD_E, GPIO.OUT)  # E

    # safe starting state
    GPIO.output(self.LCD_E, 0)        # set low as idle state
    GPIO.setup(self.LCD_RS, GPIO.OUT) # RS

    # initialize LCD data pins for output, idle low
    GPIO.setup(self.LCD_D4, GPIO.OUT) # DB4
    GPIO.output(self.LCD_D4, 0)
    GPIO.setup(self.LCD_D5, GPIO.OUT) # DB5
    GPIO.output(self.LCD_D5, 0)
    GPIO.setup(self.LCD_D6, GPIO.OUT) # DB6
    GPIO.output(self.LCD_D6, 0)
    GPIO.setup(self.LCD_D7, GPIO.OUT) # DB7
    GPIO.output(self.LCD_D7, 0)
   
    # Initialise display into 4 bit mode, using recommended delays
    self.lcd_byte(0x33, self.LCD_CMD, self.DEL_INITNEXT, self.DEL_INITMID)
    self.lcd_byte(0x32, self.LCD_CMD, self.DEL_INITNEXT)
   
    # Now perform remainder of display init in 4 bit mode - IMPORTANT!
    # These steps MUST be exactly as follows, as OLEDs in particular are rather fussy
    self.lcd_byte(0x28, self.LCD_CMD, self.DEL_INITNEXT)    # two lines and correct font
    self.lcd_byte(0x08, self.LCD_CMD, self.DEL_INITNEXT)    # display OFF, cursor/blink off
    self.lcd_byte(0x01, self.LCD_CMD, self.DEL_POSTCLEAR)   # clear display, waiting for longer delay
    self.lcd_byte(0x06, self.LCD_CMD, self.DEL_INITNEXT)    # entry mode set

    # extra steps required for OLED initialisation (no effect on LCD)
    self.lcd_byte(0x17, self.LCD_CMD, self.DEL_INITNEXT)    # character mode, power on

    self.lcd_byte(0x0C, self.LCD_CMD, self.DEL_INITNEXT)    # display on, cursor/blink off

    self.clear()

  def clear(self):
    self.lcd_byte(0x01, self.LCD_CMD) # 000001 Clear display

  @staticmethod
  def gpio_cleanup():
    GPIO.cleanup()

  # =======================================================================
  # Low level routine to output a byte of data to the LCD display
  # over the 4 bit interface. Two nibbles are sent, one after the other.
  # post_delay specifies optional delay to cover busy periods
  # mid_delay specifies optional delay between 4 bit nibbles (special case)
  # mode = True for character, False for command
  def lcd_byte(self, byteVal, mode, post_delay = 0, mid_delay = 0):
    # convert incoming value into 8 bit array, padding as required
    bits = bin(byteVal)[2:].zfill(8)

    # set mode
    GPIO.output(self.LCD_RS, mode)

    # Output the four High bits
    GPIO.output(self.LCD_D7, int(bits[0]))
    GPIO.output(self.LCD_D6, int(bits[1]))
    GPIO.output(self.LCD_D5, int(bits[2]))
    GPIO.output(self.LCD_D4, int(bits[3]))

    self.lcd_toggle_enable()

    # Wait for extra mid delay if specified (special case)
    if mid_delay > 0:
      time.sleep(mid_delay)

    # Output the four Low bits
    GPIO.output(self.LCD_D7, int(bits[4]))
    GPIO.output(self.LCD_D6, int(bits[5]))
    GPIO.output(self.LCD_D5, int(bits[6]))
    GPIO.output(self.LCD_D4, int(bits[7]))

    self.lcd_toggle_enable()

    # Wait for extra post delay if specified (covers busy period)
    if post_delay > 0:
      time.sleep(post_delay)

  def lcd_toggle_enable(self):
    # Toggle 'Enable' pin, wrapping with minimum delays
    time.sleep(self.EDEL_TAS)   
    GPIO.output(self.LCD_E, True) 
    time.sleep(self.EDEL_PWEH)
    GPIO.output(self.LCD_E, False) 
    time.sleep(self.EDEL_TAH)     

  # Send message to display
  # justify = left (default), right, or center
  def lcd_string(self, message, justify="left"):
    # Send string to display
    if justify == "right":
      message = message.rjust(self.LCD_WIDTH," ")
    elif justify == "center":
      message = message.center(self.LCD_WIDTH," ")
    else:
      message = message.ljust(self.LCD_WIDTH," ")

    for i in range(self.LCD_WIDTH):
      self.lcd_byte(ord(message[i]), self.LCD_CHR)

  def line1(self, message="", justify="left"):
    self.lcd_byte(self.LCD_LINE_1, self.LCD_CMD)
    self.lcd_string(message, justify)

  def line2(self, message="", justify="left"):
    self.lcd_byte(self.LCD_LINE_2, self.LCD_CMD)
    self.lcd_string(message, justify)

  @staticmethod
  def close(self, clear=False):
    if clear:
      self.clear()

    GPIO.cleanup()
