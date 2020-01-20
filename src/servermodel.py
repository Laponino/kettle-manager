import requests
import tflite_runtime.interpreter as tflite
import numpy as np


class ServerModel:
    def __init__(self, device_id):
        self.device_id = device_id
        self.fetch_model()

    def fetch_model(self):
        params = { "device_id": self.device_id }
        resp = requests.get("http://40.76.200.165/model", params=params)
        with open("temp/model.tfl", "wb") as f:
            f.write(resp.content)

        self.interpreter = tflite.Interpreter(model_path="temp/model.tfl")
        self.interpreter.allocate_tensors()

    def train(self, X, y):
        raise NotImplementedError("Not implemented yet")

    def predict(self, volume, temp):
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        # Test model on random input data.
        input_shape = input_details[0]['shape']
        input_data = np.array(temp, dtype=np.float32).reshape(-1, 1)
        self.interpreter.set_tensor(input_details[0]['index'], input_data)

        self.interpreter.invoke()

        # The function `get_tensor()` returns a copy of the tensor data.
        # Use `tensor()` in order to get a pointer to the tensor.
        output_data = self.interpreter.get_tensor(output_details[0]['index'])
        return output_data

if __name__ == "__main__":
    model = ServerModel(1)
    print(model.predict(1.5, 400))
