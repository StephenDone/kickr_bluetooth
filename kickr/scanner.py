import bleak

def device_filter(d, ad):
            found = d.name and d.name.startswith('KICKR BIKE') and ad.service_uuids is not None
            if(found):
                print(f'Found KICKR with name "{ad.local_name}", advertising...')
                for uuid in ad.service_uuids:
                     print(f'  {uuid}  {bleak.uuids.uuidstr_to_str(uuid)}')
                print()
            return found

async def find_kickr():
    print("Scanning for device...")
    kickr_device = await bleak.BleakScanner.find_device_by_filter( device_filter )
    if kickr_device == None: print("KICKR not found")
    return kickr_device

