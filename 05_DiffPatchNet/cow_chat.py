import asyncio
import cowsay

clients = {}

async def chat(reader, writer):
    while (True):
        send = asyncio.create_task(reader.readline())
        done, pending = await asyncio.wait([send], return_when=asyncio.ALL_COMPLETED)
        message = ""
        for q in done:
            if q is send:
                message = q.result().decode().split()
        if (message[0] == 'cows'):
            writer.write(f"{cowsay.list_cows()}\n".encode())
            await writer.drain()
        elif (message[0] == 'who'):
            writer.write(f"{clients}\n".encode())
            await writer.drain()
        elif (message[0] == 'login'):
            if (message[1] in cowsay.list_cows()):
                me = message[1]
                print(me)
                clients[me] = asyncio.Queue()
                break

    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                for out in clients.values():
                    if out is not clients[me]:
                        await out.put(f"{me} {q.result().decode().strip()}")
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())