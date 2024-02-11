from convert import ToString, ToHex

async def read(client):
    print('DEVICE INFORMATION')
    devinfo_svc = client.services.get_service('0000180a-0000-1000-8000-00805f9b34fb')

    for char in devinfo_svc.characteristics:
        print(f"  {char.uuid} {char.description:<25} {ToString(await client.read_gatt_char(char))}")

    print()
