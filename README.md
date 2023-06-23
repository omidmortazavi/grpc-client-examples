# gRPC Service Example

This is an example application demonstrating a TLS encrypted client-server communication using the gRPC framework in Python. The service offers three operations: PrintMethod, GetRunningConfig, and PassObject. The client code interacts with the service by invoking these operations.

The service supports the following operations:

print_method: Accepts a text message from the client and echoes it back as a response.

pass_object: Accepts a serialized object from the client. The object is deserialized and logged on the server.

get_running_config: Accepts device parameters (device type, IP, username, and password) from the client and connects to the specified network device using Netmiko. It retrieves the running configuration of the device and returns it as a response.


## Generating Python Files

To generate the Python files from the `service.proto` file, follow these steps:

1. Make sure you have the `service.proto` file in the root directory of the project.

2. Open a terminal or command prompt and navigate to the project directory.

3. Run the following command to generate the Python files:

   ```
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto
   ```


This command uses the `grpc_tools.protoc` module to invoke the Protocol Buffers compiler (`protoc`) and generate the Python files.

4. After running the command, you should see two new files generated: `service_pb2.py` and `service_pb2_grpc.py`. These files contain the generated code for the gRPC service and message classes.

## Usage

To run the gRPC application, follow these steps:

1. Ensure that you have generated the Python files as mentioned in the previous section.

2. Start the server by running the `server.py` script:

The server will start and listen on port 50051.

3. In a separate terminal or command prompt, run the `client.py` script to interact with the server:


The client code demonstrates three operations:

1. `echo_test()`: It sends a text message to the server, which echoes it back as a response.

2. `serialize_object()`: It serializes a Python object, encodes it as a base64 string, and sends it to the server. The server deserializes the object and logs it.

3. `get_running_config()`: It sends device parameters (device type, IP, username, and password) to the server. The server connects to the specified network device using Netmiko, retrieves the running configuration, and returns it as a response.

Ensure that the server is running before executing the client code.

## Additional Notes

- The `certificates` directory contains the sample certificates used for TLS encryption. You may replace them with your own certificates for secure communication.

- Make sure the server and client are running on the same host for local testing. If you want to connect to a remote server, update the address in the client script accordingly.

- Feel free to explore and modify the `service.proto` file to define your own service and message types.

For more information on gRPC and Protocol Buffers, refer to the official documentation:

- gRPC: https://grpc.io
- Protocol Buffers: https://developers.google.com/protocol-buffers

# License
This project is licensed under the MIT License.

# Acknowledgments
The gRPC service and client code is based on the gRPC framework and the Netmiko library. Special thanks to the contributors of these projects for their valuable work.