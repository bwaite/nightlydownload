#!/usr/bin/env python3

import dbus
from datetime import datetime

stop_time = datetime.today().replace(hour=7, minute=30, second=0)

bus = dbus.SystemBus()

proxy = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')

iface = dbus.Interface(proxy, 'org.freedesktop.systemd1.Manager')


def check_downloading():
    for unit in iface.ListUnits():

        (unit_id, desc, load_state, active_state, sub_state,
         job_type, obj_path, _, _, _) = unit

        if str(unit_id) == 'hello.timer':
            print(str(unit) + "\n")
            # If the time is up
            if datetime.datetime.now() > stop_time:
                iface.StopUnit(unit_id, "replace")
                # iface.PowerOff()

check_downloading()
