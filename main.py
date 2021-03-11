import pymem
import pymem.process
import re
import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send("ok\n" + message)
        if message == "wallhackenable":
            toggleWallhack(True)
        elif message == "wallhackdisable":
            toggleWallhack(False)
        elif message == "radarhackenable":
            toggleRadarhack(True)
        elif message == "radarhackdisable":
            toggleRadarhack(False)
        elif message == "moneyhackenable":
            toggleMoney(True)
        elif message == "moneyhackdisable":
            toggleMoney(False)
        else:
            await websocket.send("Could not execute!")

start_server = websockets.serve(echo, "localhost", 1337)

pm = pymem.Pymem('csgo.exe')
client = pymem.process.module_from_name(pm.process_handle, 'client.dll')

clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)

def toggleWallhack(toggled):
    address = client.lpBaseOfDll + re.search(rb'\x83\xF8.\x8B\x45\x08\x0F', clientModule).start() + 2
    if toggled == True:
        pm.write_uchar(address, 1)
    else:
        pm.write_uchar(address, 2)

def toggleMoney(toggled):
    address = client.lpBaseOfDll + re.search(rb'.\x0C\x5B\x5F\xB8\xFB\xFF\xFF\xFF', clientModule).start()
    if toggled == True:
        pm.write_uchar(address, 0xEB)
    else:
        pm.write_uchar(address, 0x75) 

def toggleRadarhack(toggled):
    address = client.lpBaseOfDll + re.search(rb'\x80\xB9.{5}\x74\x12\x8B\x41\x08', clientModule).start() + 6
    if toggled == True:
        pm.write_uchar(address, 2)
    else:
        pm.write_uchar(address, 0)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
pm.close_process()