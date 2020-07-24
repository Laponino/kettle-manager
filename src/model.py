import requests
import os
import tflite_runtime.interpreter as tflite
import numpy as np


class ServerModel:
    def __init__(self, device_id):
        self.device_id = device_id
        self.fetch_model()
        self.server = "http://40.76.200.165/"
        self.train_data_path = os.path.join("temp", "out.csv")       

    def fetch_model(self):
        print("Fetching model for device_id...")
        params = { "device_id": self.device_id }
        try:
            resp = requests.get("http://40.76.200.165/model", params=params, timeout=5)
            with open("temp/model.tfl", "wb") as f:
                f.write(resp.content)
        except:
            print("Failed to reach server, using local model")

        self.interpreter = tflite.Interpreter(model_path="temp/model.tfl")
        self.interpreter.allocate_tensors()

    def train(self, volume, temps, times):
        Temps = np.array(temps).reshape(-1, 1)
        Volumes = np.ones_like(Temps) * volume
        X = np.hstack((Volumes, Temps))
        y = np.array(times).reshape(-1, 1)
        Xy = np.hstack((X, y))
        np.savetxt(self.train_data_path, Xy, delimiter=",")
        params = {"device_id": self.device_id}
        files = {"out.csv": open(self.train_data_path, "rb")} 
        requests.post(self.server + "data", params=params, files=files)

    def predict(self, volume, temp):
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        # Test model on random input data.
        input_shape = input_details[0]['shape']
        input_data = np.array([volume, temp], dtype=np.float32).reshape((1, 2))
        self.interpreter.set_tensor(input_details[0]['index'], input_data)

        self.interpreter.invoke()

        # The function `get_tensor()` returns a copy of the tensor data.
        # Use `tensor()` in order to get a pointer to the tensor.
        output_data = self.interpreter.get_tensor(output_details[0]['index'])
        return output_data

if __name__ == "__main__":
    model = ServerModel(1)
    print(model.predict(1.5, 400))
