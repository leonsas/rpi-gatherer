import os
import glob
import time, datetime
import tempodb

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    temp_c, temp_f = None, None
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
    return temp_c, temp_f

def init_client():
    fname = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir)) + "/tempodb_keys"
    with open(fname,'r') as f:
        api_key = f.readline().strip()
        api_secret = f.readline().strip()

    print api_key, api_secret
    return tempodb.Client(api_key, api_secret)

def main():
    temp_c, temp_f = read_temp()
    now = datetime.datetime.now()
    data = []

    if temp_c:
        data.append({'key': 'sensor-type:temperature.temp-unit:C.1',
                    'v': temp_c
                    })

    if temp_f:
        data.append({'key': 'sensor-type:temperature.temp-unit:F.1',
                    'v': temp_f
                    })

    client = init_client()
    print now, data
    client.write_bulk(now, data)

if __name__ == '__main__':
    main()


