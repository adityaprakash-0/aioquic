import asyncio
from aioquic.asyncio import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import StreamDataReceived

class ClientProtocol(QuicConnectionProtocol):
    def __init__(self, *args, message=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message

    def quic_event_received(self, event):
        if isinstance(event, StreamDataReceived):
            print(f"\nReceived:\n{event.data.decode()}") 
            '''Here data received will be in one go to solve - slow down sending from server.
            or can use this other method on client side displayed below.'''
            # buffer = ""
            # buffer += event.data.decode()
            # for line in buffer.splitlines():
            #     print("Line:", line)
            

async def main():
    configuration = QuicConfiguration(
        is_client=True,
        alpn_protocols=["hq-29"]
    )
    
    configuration.verify_mode = False  # Disable cert verification for local server
    
    async with connect("127.0.0.1", 4433, configuration=configuration, create_protocol=ClientProtocol) as client:
        stream_id = client._quic.get_next_available_stream_id()
        message = str(input("Enter a number: "))
        client._quic.send_stream_data(stream_id, message.encode(), end_stream=True)
        await asyncio.sleep(2)  # Give time for response

if __name__ == "__main__":
    asyncio.run(main())

