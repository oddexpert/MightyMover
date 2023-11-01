import mighty
import bluetooth
import time

time.sleep(1)

mover = mighty.MightyMover()

mover.stopMover()


server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]
uuid = mover.service_uuid

bluetooth.advertise_service(server_sock, "MyBLEServer", service_id=uuid, service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS], profiles=[bluetooth.SERIAL_PORT_PROFILE])

print(f"Waiting for a connection on RFCOMM channel {port}...")
client_sock, client_info = server_sock.accept()

print("Accepted connection from", client_info)
while True:
    try:
        mover.handle_client(client_sock)
        #time.sleep(1)
    except KeyboardInterrupt:
        exit()

client_sock.close()
server_sock.close()
