import asyncio
from bleak import BleakClient

import kickr.uuids
import kickr.scanner
import kickr.devinfo as devinfo
import kickr.tilt as tilt
import kickr.chosen_gear as chosen_gear
import kickr.buttons as buttons
import kickr.user_data as user_data
import kickr.cycling_power as cycling_power
import kickr.cycling_power_extension as power_extension

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

        await devinfo.read(client)

        await user_data.read(client)

        await power_extension.start_notify(client)
        await power_extension.power_extension_tests(client)
        await power_extension.stop_notify(client)

        await cycling_power.cycling_power_tests(client)
        await cycling_power.start_notify(client)
        await asyncio.sleep(1)
        await cycling_power.stop_notify(client)

        await tilt.start_notify(client)
        await tilt.read_tests(client)
        await tilt.stop_notify(client)

        await chosen_gear.start_notify(client)
        await asyncio.sleep(3)
        await chosen_gear.stop_notify(client)

        await buttons.start_notify(client)
        await asyncio.sleep(3)
        await buttons.stop_notify(client)

    finally:
        await client.disconnect()

asyncio.run(main())

