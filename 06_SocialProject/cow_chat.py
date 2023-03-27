import asyncio
import cowsay

clients = {}
cows_list = cowsay.list_cows()
async def chat(reader, writer):
    is_registered = False
    me = ""
    buffQueue = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(buffQueue.get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                message = q.result().decode().split()
                if (len(message) < 1):
                    continue
                elif (message[0] == 'cows'):
                    writer.write(f"{cows_list}\n".encode())
                    await writer.drain()
                elif (message[0] == 'who'):
                    writer.write(f"Registered users: {', '.join(clients.keys())}\n".encode())
                    await writer.drain()
                elif (message[0] == "say"):
                    if (not(is_registered)):
                        writer.write("You are not registered!\n".encode())
                        await writer.drain()
                        continue
                    if (message[1] in clients.keys()):
                        await clients[message[1]].put(f"From: {me}\n {cowsay.cowsay((' '.join(message[2:])).strip(), cow=me)}")
                        writer.write("Message send!\n".encode())
                        await writer.drain()
                    else:
                        writer.write("No user with this name\n".encode())
                        await writer.drain()
                elif (message[0] == 'yield'):
                    if (not(is_registered)):
                        writer.write("You are not registered!\n".encode())
                        await writer.drain()
                        continue
                    for out in clients.values():
                        if out is not clients[me]:
                            await out.put(f"From: {me}\n {cowsay.cowsay(' '.join(message[1:]).strip(), cow=me)}")
                    writer.write("Message send!\n".encode())
                    await writer.drain()
                elif (message[0] == 'login' and not(is_registered)):
                    if (message[1] in cows_list):
                        me = message[1]
                        print("Registered: ", me)
                        clients[me] = asyncio.Queue()
                        cows_list.remove(message[1])
                        writer.write("You are registered!\n".encode())
                        await writer.drain()
                        is_registered = True
                        receive.cancel()
                        receive = asyncio.create_task(clients[me].get())
                    else:
                        writer.write("Invalid name!\n".encode())
                        await writer.drain()
                elif (message[0] == "quit"):
                    send.cancel()
                    receive.cancel()
                    if is_registered:
                        del clients[me]
                        print("Unregistered: ", me)
                        cows_list.append(me)
                    writer.close()
                    await writer.wait_closed()
                    return
                else:
                    writer.write("Wrong command!\n".encode())
                    await writer.drain()
            elif q is receive and is_registered:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    if me:
        print("Unregistered: ", me)
        cows_list.append(me)
        del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())