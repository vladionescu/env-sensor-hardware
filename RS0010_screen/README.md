For controlling a SparkFun 16x2 OLED display utilizing the RS0010 controller instead of the popular HD44780.

### Dependencies

This requires RPi.GPIO, a poorly named package found in [PyPi](https://pypi.python.org/pypi/RPi.GPIO) and Raspbian's Apt:

```
$ pip install RPi.GPIO
```

or

```
$ sudo apt install python-rpi.gpio
```

### Credits

Based on [Matt Hawkin's lcd_16x2.py](http://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/).

Using robertcx's and Paul Carpenter's improvements from [this RaspberryPi forum thread](https://www.raspberrypi.org/forums/viewtopic.php?t=68055&p=514131).
