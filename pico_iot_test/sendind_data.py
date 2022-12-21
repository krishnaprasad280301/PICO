def main():
    import sys
    shouldRun = str(input('Run? (y/n): ')).lower()
    if shouldRun != 'y':
        sys.exit(1)
    del sys  # make space in memory

    from lib.at_client.io_util import read_settings
    ssid, password, atSign = read_settings()
    del read_settings

    print('Connecting to WiFi %s...' % ssid)
    from lib.wifi import init_wlan
    init_wlan(ssid, password)
    del ssid, password, init_wlan

    from lib.at_client.at_client import AtClient
    atClient = AtClient(atSign)
    del AtClient
    atClient.pkam_authenticate(verbose=True)

    value = 0
    from machine import Pin, ADC
    from utime import sleep
    xAxis = ADC(Pin(26))
    yAxis = ADC(Pin(27))
    button = Pin(22, Pin.IN, Pin.PULL_UP)

    while True:
        xValue = xAxis.read_u16()
        yValue = yAxis.read_u16()
        buttonValue = button.value()
        xStatus = "middle"
        yStatus = "middle"
        buttonStatus = "not pressed"
        if xValue <= 600:
            xStatus = "left"
        elif xValue >= 60000:
            xStatus = "right"
        if yValue <= 600:
            yStatus = "up"
        elif yValue >= 60000:
            yStatus = "down"
        if buttonValue == 0:
            buttonStatus = "pressed"

        data = atClient.put_public('joystick', str("X: " + xStatus + ", Y: " + yStatus + " -- button " + buttonStatus)) # needs to be updated with the atsigns
        #print data

        print("X: " + xStatus + ", Y: " + yStatus + " -- button " + buttonStatus)
        utime.sleep(0.1)



if __name__ == '__main__':
    main()