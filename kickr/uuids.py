import bleak

kickr_virtual_bike_svc          = 'a026ee0d-0a7d-4ab3-97fa-f1500f9feb8b'
kickr_buttons                   = 'a026e03c-0a7d-4ab3-97fa-f1500f9feb8b'
kickr_chosen_gear               = 'a026e03a-0a7d-4ab3-97fa-f1500f9feb8b'
kickr_groupset                  = 'a026e039-0a7d-4ab3-97fa-f1500f9feb8b'

kickr_cycling_power_extension   = 'a026e005-0a7d-4ab3-97fa-f1500f9feb8b'

kickr_tilt_svc                  = 'a026ee0b-0a7d-4ab3-97fa-f1500f9feb8b'
kickr_tilt_characteristic       = 'a026e037-0a7d-4ab3-97fa-f1500f9feb8b'

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
