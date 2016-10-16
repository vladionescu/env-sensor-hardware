# Environmental Sensor Hardware

Attempting to use an [Si7021 Humidity and Temperature Sensor](https://www.sparkfun.com/products/13763) and a [TSL2561 Luminosity Sensor](https://www.sparkfun.com/products/12055) to get environmental stats and output them on a 16x2 OLED screen.

Currently prototyping on a Raspberry Pi 2.

### Future plans include:

* Run everything from an Arduino Micro clone
* Use an [ESP8266](https://www.sparkfun.com/products/13678) to send data to a sink at regular intervals
* Add a [Capacitive Soil Moisture Sensor](https://www.dfrobot.com/wiki/index.php/Capacitive_Soil_Moisture_Sensor_SKU:SEN0193)
* Connect two 5V solar panels to an [MPPT Solar Charger](https://www.sparkfun.com/products/12885) powering the Ardunio+ESP and a [2 Ah LiPo](https://www.sparkfun.com/products/8483) battery.
* Use the data to create pretty charts to study correlations between temperature, humidity, soil moisture, and sunlight

### Installation

Setup a virtualenv, enter it and install the requirements.

1. `$ sudo apt install python-pip python-virtualenv`
2. `$ virtualenv --python $(which python2) venv`
3. `$ source venv/bin/activate`
4. `$ pip install -r requirements.txt`

To exit the virtualenv simply `$ deactivate` from within the project dir.

### Resources:

* SparkFun datasheets and hookup tutorials
* [Raspberry Pi B+ Pinout](http://www.raspberrypi-spy.co.uk/wp-content/uploads/2012/06/Raspberry-Pi-GPIO-Layout-Model-B-Plus-rotated-2700x900.png)
* or [Raspberry Pi 3 Pinout](https://www.element14.com/community/servlet/JiveServlet/previewBody/73950-102-10-339300/pi3_gpio.png)

I2C:
* http://www.robot-electronics.co.uk/i2c-tutorial
* http://www.i2c-bus.org/addressing/

I2C on RPi:
* https://pypi.python.org/pypi/smbus-cffi/0.5.1
* https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
* https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial

OLED Screen:
* Script from: http://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/
* [RPi.GPIO from PyPi](https://pypi.python.org/pypi/RPi.GPIO) or Raspbian Apt `$ sudo apt install python-rpi.gpio`
* [SparkFun OLED Hookup Guide](https://learn.sparkfun.com/tutorials/oled-display-hookup-guide/all)
* [YouTube - Using a 16x2 LCD Display with a Raspberry Pi](https://www.youtube.com/watch?v=cVdSc8VYVBM)

Temperature Sensor:
* Script from: https://github.com/ControlEverythingCommunity/SI7021/blob/master/Python/SI7021.py
* [SparkFun Temp and Humidity Sensor Hookup Guide](https://learn.sparkfun.com/tutorials/si7021-humidity-and-temperature-sensor-hookup-guide)
* [SparkFun Si7021 Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Weather/Si7021.pdf)

Luminosity Sensor:
* [SparkFun C++ Library for reference](https://github.com/sparkfun/SparkFun_TSL2561_Arduino_Library/blob/V_1.1.0/src/SparkFunTSL2561.cpp)
* [tsl2561 Python package](https://pypi.python.org/pypi/tsl2561) which requires [Adafruit-GPIO Python package](https://pypi.python.org/pypi/Adafruit-GPIO/1.0.0)
* https://github.com/janheise/TSL2561 which requires [quick2wire](https://github.com/quick2wire/quick2wire-python-api)
