#!/usr/bin/python3
# ddcutil-dasbus-signal-receiver.py
# ---------------------------------
# Python dasbus example of receiving signals from ddcutil-service
#
# Copyright (C) 2023, Michael Hamilton
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
import base64
import time
# dasbus seems to be recent, popular and actively supported.
# (perhaps also look at dbus-next)

from collections import namedtuple

from dasbus.connection import SessionMessageBus
from dasbus.loop import EventLoop

bus = SessionMessageBus()

ddcutil_proxy = bus.get_proxy(
    "com.ddcutil.DdcutilService",  # The bus name
    "/com/ddcutil/DdcutilObject",  # The object name
)

def callback_connected_displays_changed(edid_encoded: str, event_type: int, flags: int):
    print(f"ConnectedDisplaysChanged Callback called {event_type=} {flags=} {edid_encoded:.30}...")

def callback_vcp_value_changed(display_num:int, edid_encoded: str, vcp_code: int, new_value: int,
                               client_name: str, client_context: str, flags: int):
    print(f"VcpValueChanged Callback called {display_num=} {edid_encoded=:.30}... {vcp_code=} {new_value=} "
          f"{client_name=} {client_context=}")

print(f"{ddcutil_proxy.ServiceInterfaceVersion=}")

# Wait on signal
ddcutil_proxy.ConnectedDisplaysChanged.connect(callback_connected_displays_changed)

ddcutil_proxy.VcpValueChanged.connect(callback_vcp_value_changed)

loop = EventLoop()
loop.run()


