import asyncio
import bleak
from bleak import BleakClient
from bleak import BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

import kickr.uuids
import kickr.scanner
import kickr.devinfo
import kickr.tilt as tilt
import kickr.chosen_gear as chosen_gear
import kickr.buttons as buttons

from convert import ToString, ToHex

ShowCharacteristicDescriptors = False

async def main():
    kickr.uuids.register_uuids()

    device = await kickr.scanner.find_kickr()
    if device == None: exit()

    print(f"Connecting to device {device.name}...")
    client = BleakClient(device)
    try:
        await client.connect()

        if(client.is_connected):
            print(f"Connected with address {client.address}\r\n")
        else:
            return
        
        kickr.uuids.print_uuids(client)

        await kickr.devinfo.read(client)

        await tilt.start_notify(client)
        await tilt.read_tests(client)
        await tilt.stop_notify(client)

        await chosen_gear.start_notify(client)
        await asyncio.sleep(10)
        await chosen_gear.stop_notify(client)

        await buttons.start_notify(client)
        await asyncio.sleep(10)
        await buttons.stop_notify(client)

    finally:
        await client.disconnect()

asyncio.run(main())
