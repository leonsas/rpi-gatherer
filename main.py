import os
import glob
import time, datetime
from phant import Phant

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
    return temp_c

def init_client():
    fname = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir)) + "/data_sparkfun_keys"

    with open(fname,'r') as f:
        public_key = f.readline().strip()
        private_key = f.readline().strip()

    return Phant(public_key, 'c',private_key=private_key)

def main():
    temp_c = read_temp()

    if temp_c:
        client = init_client()
        print temp_c
        client.log(temp_c)

if __name__ == '__main__':
    main()


