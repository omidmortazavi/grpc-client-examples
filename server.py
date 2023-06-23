import base64
import grpc
import logging
import pickle
import service_pb2
import service_pb2_grpc

from concurrent import futures
from netmiko import ConnectHandler
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s"
)

logger = logging.getLogger("server_log")
logger.addHandler(logging.FileHandler("server.log"))
logger.addHandler(RichHandler())


class AutomationServiceServicer(service_pb2_grpc.AutomationServiceServicer):
    """Implementation of the AutomationServiceServicer."""

    def print_method(self, request, context):
        """PrintMethod gRPC service implementation.

        Args:
            request (ServerRequest): The request object.
            context (grpc.ServicerContext): The context object.

        Returns:
            ServerResponse: The response object.
        """
        data = request.data
        logger.info("Received text: %s", data)
        result = "Echo: " + data
        return service_pb2.ServerResponse(result=result)

    def get_running_config(self, request, context):
        """GetRunningConfig gRPC service implementation.

        Args:
            request (ServerRequest): The request object.
            context (grpc.ServicerContext): The context object.

        Returns:
            ServerResponse: The response object.
        """
        device = {
            "device_type": request.device_type,
            "ip": request.ip,
            "username": request.username,
            "password": request.password,
        }
        try:
            logger.info(device)
            logger.info(f"Connecting to Device: {device['ip']}")
            connection = ConnectHandler(**device)
            output = connection.send_command("show running-config")
            connection.disconnect()
            logger.info("Running config:")
            logger.info(output)
            result = "Running config:\n" + output
        except Exception as e:
            result = "Error: " + str(e)

        return service_pb2.ServerResponse(result=result)

    def pass_object(self, request, context):
        """PassObject gRPC service implementation.

        Args:
            request (ServerRequest): The request object.
            context (grpc.ServicerContext): The context object.

        Returns:
            ServerResponse: The response object.
        """
        encoded_object = request.data

        # Decode the base64-encoded string
        serialized_object = base64.b64decode(encoded_object)

        # Deserialize the object using pickle
        my_object = pickle.loads(serialized_object)

        logger.info("Received object: {}".format(my_object))
        logger.info("Received object Type: {}".format(type(my_object)))

        result = "Object received"

        return service_pb2.ServerResponse(result=result)

    def execute_nornir_task(self, request, context):
        """Deserializes the Nornir inventory, performs the Nornir task, and sends the result back to the client."""
        # Decode the base64-encoded inventory
        decoded_inventory = base64.b64decode(request.inventory)

        # Deserialize the inventory
        deserialized_inventory = pickle.loads(decoded_inventory)

        inventory_string = deserialized_inventory.dict()

        # Print the Nornir inventory received from the client
        logger.info(f"Nornir inventory received from client: {inventory_string}")

        # TODO: Execute the Nornir task

        # Return the response
        response = service_pb2.ServerResponse(result="Nornir task executed successfully!")
        return response

def serve():
    """Starts the gRPC server and listens for incoming requests."""
    try:
        with open("certificates/server.key", "rb") as key_file:
            private_key = key_file.read()

        server_credentials = grpc.ssl_server_credentials(
            [(private_key, open("certificates/server.crt", "rb").read())]
        )
        server = grpc.server(futures.ThreadPoolExecutor())
        service_pb2_grpc.add_AutomationServiceServicer_to_server(
            AutomationServiceServicer(), server
        )
        server.add_secure_port("[::]:50051", server_credentials)
        server.start()
        print("Server started. Listening on port 50051.")
        server.wait_for_termination()
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    serve()
