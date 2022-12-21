def main():
    # read settings.json
 from lib.at_client.io_util import read_settings
 ssid, password, atSign = read_settings()
 del read_settings

 # connect to wifi
 print('Connecting to WiFi %s...' % ssid)
 from lib.wifi import init_wlan
 init_wlan(ssid, password)
 del ssid, password, init_wlan

 # authenticate into server
 from lib.at_client.at_client import AtClient
 atClient = AtClient(atSign, writeKeys=True)
 del AtClient
 atClient.pkam_authenticate(verbose=True)

 #sned data
 key = 'led'
 value = 0

 key1 = 'joystick'
 value1= 10

 for i in range(100):
    if value==1:
        value=0
        value1=80
    elif value==0:
        value=1
        value1=90
    atClient.put_public(key, str(value))
    atClient.put_public(key1, str(value1))

if __name__ == '__main__':
    main()