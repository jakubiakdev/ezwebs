import pymem
import pymem.process
import re
import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send("ok\n" + message)
        if message == "wallhackenable":
            toggleWallhack("enabled")
        elif message == "wallhackdisable":
            toggleWallhack("disabled")
        else:
            await websocket.send("Could not execute!")

start_server = websockets.serve(echo, "localhost", 1337)

pm = pymem.Pymem('csgo.exe')
client = pymem.process.module_from_name(pm.process_handle, 'client.dll')

clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)

def toggleWallhack(toggled):
    address = client.lpBaseOfDll + re.search(rb'\x83\xF8.\x8B\x45\x08\x0F', clientModule).start() + 2
    print(toggled)
    if toggled == 'enabled':
        pm.write_uchar(address, 1)
    else:
        pm.write_uchar(address, 2)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
pm.close_process()