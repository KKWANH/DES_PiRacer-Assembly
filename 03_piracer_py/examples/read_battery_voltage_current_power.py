# Copyright (C) 2022 twyleg
import time
from piracer.vehicles import PiRacerStandard, PiRacerPro


def print_energy_report():
    battery_voltage = piracer.get_battery_voltage()
    battery_current = piracer.get_battery_current()
    power_consumption = piracer.get_power_consumption()

    print('Battery voltage={0:0>6.3f}V, current={1:0>8.3f}mA, power={2:0>6.3f}W'.format(battery_voltage, battery_current,
                                                                                power_consumption))


if __name__ == '__main__':
    piracer = PiRacerPro()
    # piracer = PiRacerStandard()

    print("Powertrain off")
    print_energy_report()
    time.sleep(1.0)

    print("Powertrain at 30%")
    piracer.set_throttle_percent(0.3)
    time.sleep(3.0)
    print_energy_report()

    print("Powertrain at 100%")
    piracer.set_throttle_percent(1.0)
    time.sleep(3.0)
    print_energy_report()

    print("Powertrain off")
    piracer.set_throttle_percent(0.0)
    time.sleep(3.0)
    print_energy_report()
