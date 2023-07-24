# Copyright (C) 2022 twyleg
import os
import pathlib
import time
from piracer.vehicles import PiRacerBase, PiRacerStandard, PiRacerPro


FILE_DIR = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))


def print_battery_report(vehicle: PiRacerBase):
    battery_voltage = vehicle.get_battery_voltage()
    battery_current = vehicle.get_battery_current()
    power_consumption = vehicle.get_power_consumption()

    display = vehicle.get_display()

    output_text = 'U={0:0>6.3f}V\nI={1:0>8.3f}mA\nP={2:0>6.3f}W'.format(battery_voltage, battery_current,
                                                                                power_consumption)

    display.fill(0)
    display.text(output_text, 0, 0, 'white', font_name=FILE_DIR / 'fonts/font5x8.bin')
    display.show()


if __name__ == '__main__':

    piracer = PiRacerPro()
    # piracer = PiRacerStandard()

    while True:
        print_battery_report(piracer)
        time.sleep(0.5)
