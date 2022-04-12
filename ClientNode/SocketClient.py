import websockets


class ClientSocket:
    def __init__(self, url):
        self.url = url

    def connent(self):
        try:
            async with websockets.connect(self.url) as websocket:
                websocketss.append(websocket)
                print(websocketss)
                while True:
                    # producer = asyncio.create_task()
                    # consumer = asyncio.create_task()
                    # await asyncio.gather(producer, consumer)
                    consumer_task = asyncio.ensure_future(
                        receiving(websocket)
                    )
                    producer_task = asyncio.ensure_future(
                        sending(websocket)
                    )
                    done, pending = await asyncio.wait(
                        [consumer_task, producer_task],
                        return_when=asyncio.FIRST_COMPLETED,
                    )
                    for task in pending:
                        task.cancel()
        except Exception as e:
            print(e)
