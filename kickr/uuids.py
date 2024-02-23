import bleak

def normalize_wahoo_uuid(uuid) -> str:
    return f'a026{uuid:04x}-0a7d-4ab3-97fa-f1500f9feb8b'

kickr_virtual_bike_svc          = normalize_wahoo_uuid(0xee0d)
kickr_buttons                   = normalize_wahoo_uuid(0xe03c)
kickr_chosen_gear               = normalize_wahoo_uuid(0xe03a)
kickr_groupset                  = normalize_wahoo_uuid(0xe039)

kickr_cycling_power_extension   = normalize_wahoo_uuid(0xe005)

kickr_tilt_svc                  = normalize_wahoo_uuid(0xee0b)
kickr_tilt_characteristic       = normalize_wahoo_uuid(0xe037)

def register_uuids():
    bleak.uuids.register_uuids({
        kickr_virtual_bike_svc:         '### KICKR Virtual Bike',
        kickr_buttons:                  '### KICKR Buttons', 
        kickr_chosen_gear:              '### KICKR Chosen Gear', 
        kickr_groupset:                 '### KICKR Groupset',
        kickr_cycling_power_extension:  '### KICKR Cycling Power Extension',
        kickr_tilt_svc:                 '### KICKR Tilt Service',
        kickr_tilt_characteristic:      '### KICKR Tilt Characteristic'
    })

def print_uuids(client:bleak.BleakClient, ShowCharacteristicDescriptors:bool=False):
    print('KICKR SERVICES AND CHARACTERISTICS')

    for handle in client.services.services:
        svc = client.services.services[handle]
        print(f"{handle}        {svc.uuid}  {' '*44}  {svc.description}")

        for char in svc.characteristics:
            print(f"   {char.handle}     {char.uuid}  {f'{char.properties}':<44}  {char.description}")

            if(ShowCharacteristicDescriptors):
                for des in char.descriptors:
                    print(f"      {des.handle}  {des.uuid}  {' '*44}  {des.description.replace('Client Characteristic Configuration','CCCD')}")

        print()
