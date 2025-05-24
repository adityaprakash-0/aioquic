import asyncio
from aioquic.asyncio import serve
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.events import StreamDataReceived
from aioquic.quic.configuration import QuicConfiguration  

class ServerQuicProtocol(QuicConnectionProtocol):
    def quic_event_received(self, event):
        if isinstance(event, StreamDataReceived):
            num = int(event.data.decode())
            print(f"Received value:",num,'\n')
            for i in range(1,11):
                value = num*i
                message = f"{num}*{i}={value}\n"
                self._quic.send_stream_data(event.stream_id, message.encode(), end_stream=False)
            
            self._quic.send_stream_data(event.stream_id, "Ending...".encode(), end_stream=True)
            

async def main():
    config = QuicConfiguration(
        is_client=False,
        alpn_protocols=["hq-29"]
    )
    config.load_cert_chain("cert.pem", "key.pem")

    await serve(
        host="127.0.0.1",
        port=4433,
        configuration=config,  
        create_protocol=ServerQuicProtocol,
    )
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
