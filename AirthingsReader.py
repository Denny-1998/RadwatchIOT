
import bluepy.btle as btle
import argparse
import signal
import struct
import sys
import time


class Wave2():

    CURR_VAL_UUID = btle.UUID("b42e4dcc-ade7-11e4-89d3-123b93f75cba")

    def __init__(self, serial_number):
        self._periph = None
        self._char = None
        self.mac_addr = None
        self.serial_number = serial_number

    def is_connected(self):
        try:
            return self._periph.getState() == "conn"
        except Exception:
            return False

    def discover(self):
        scan_interval = 0.1
        timeout = 3
        scanner = btle.Scanner()
        for _count in range(int(timeout / scan_interval)):
            advertisements = scanner.scan(scan_interval)
            for adv in advertisements:
                if str(self.serial_number) == str(_parse_serial_number(adv.getValue(btle.ScanEntry.MANUFACTURER))):
                    print("s/n: " + str(self.serial_number))
                    print("   : " + str(_parse_serial_number(adv.getValue(btle.ScanEntry.MANUFACTURER))))
                    return adv.addr
        return None

    def connect(self, retries=10):
        tries = 0
        while (tries < retries and self.is_connected() is False):
            tries += 1
            print("tries: " + str(tries))
            if self.mac_addr is None:
                self.mac_addr = self.discover()
            try:
                self._periph = btle.Peripheral(self.mac_addr)
                self._char = self._periph.getCharacteristics(uuid=self.CURR_VAL_UUID)[0]
            except Exception:
                if tries == retries:
                    raise
                else:
                    pass

    def read(self):
        rawdata = self._char.read()
        return CurrentValues.from_bytes(rawdata)

    def disconnect(self):
        if self._periph is not None:
            self._periph.disconnect()
            self._periph = None
            self._char = None


class CurrentValues():

    def __init__(self, humidity, radon_sta, radon_lta, temperature):
        self.humidity = humidity
        self.radon_sta = radon_sta
        self.radon_lta = radon_lta
        self.temperature = temperature

    @classmethod
    def from_bytes(cls, rawdata):
        data = struct.unpack("<4B8H", rawdata)
        if data[0] != 1:
            raise ValueError("Incompatible current values version (Expected 1, got {})".format(data[0]))
        return cls(data[1]/2.0, data[4], data[5], data[6]/100.0)

    def __str__(self):
        msg = "Humidity: {} %rH, ".format(self.humidity)
        msg += "Temperature: {} *C, ".format(self.temperature)
        msg += "Radon STA: {} Bq/m3, ".format(self.radon_sta)
        msg += "Radon LTA: {} Bq/m3".format(self.radon_lta)
        return msg


def _parse_serial_number(manufacturer_data):
    try:
        (ID, SN, _) = struct.unpack("<HLH", manufacturer_data)
    except Exception:  # Return None for non-Airthings devices
        return None
    else:  # Executes only if try-block succeeds
        if ID == 0x0334:
            return SN


def _argparser():
    parser = argparse.ArgumentParser(prog="read_wave2", description="Script for reading current values from a 2nd Gen Wave product")
    parser.add_argument("SERIAL_NUMBER", type=int, help="Airthings device serial number found under the magnetic backplate.")
    parser.add_argument("SAMPLE_PERIOD", type=int, default=60, help="Time in seconds between reading the current values")
    args = parser.parse_args()
    return args


def connectAndRead(SERIAL_NUMBER):
    print (SERIAL_NUMBER)
    wave2 = Wave2(SERIAL_NUMBER)

    def _signal_handler(sig, frame):
        wave2.disconnect()
        sys.exit(0)

    signal.signal(signal.SIGINT, _signal_handler)


    wave2.connect(retries=10)
    current_values = wave2.read()
    wave2.disconnect()
    return current_values
