import joblib
import pandas as pd
import numpy as np
#from tensorflow import keras
import keras
import sys
from keras import backend as K
from apps.endpoints.models import DatosMovimiento

import tensorflow as tf
graph = tf.get_default_graph()

class AnomalyDetector:

    __instance = None

    def __init__(self):
        keras.backend.clear_session()
        path_to_artifacts = "../../research/"
        #self.graph = tf.get_default_graph()
        self.scaler = joblib.load(path_to_artifacts + "scaler.joblib")
        self.pca = joblib.load(path_to_artifacts + "pca.joblib")
        #self.model = keras.models.load_model(path_to_artifacts + "model_nn3.h5")
        self.model = keras.models.load_model(path_to_artifacts + "model_nn3.h5")
        self.if_model = joblib.load(path_to_artifacts + "isolation_model.joblib")

    def __new__(cls):
        if AnomalyDetector.__instance is None:
            AnomalyDetector.__instance = object.__new__(cls)
        return AnomalyDetector.__instance

    def preprocessing(self, input_data):
        # JSON to pandas DataFrame
        dataframe = pd.DataFrame(input_data)
        sensors = dataframe[['acc_x', 'acc_y', 'acc_z', 'gyr_x', 'gyr_y', 'gyr_z']]
        # fill missing values
        sensors = sensors.values
        sensors = self.scaler.transform(sensors)
        sensors = self.pca.transform(sensors)
        return np.array([sensors]), dataframe

    def predict(self, input_data):
        #K.clear_session()

        keras.backend.clear_session()
        # Autoencoder predicted and generate difference with real data
        #with self.graph.as_default():
        diff = self.model.predict(input_data) - input_data
        # Isolation Forest predicted
        return self.if_model.predict(diff[0].reshape((1,9)))

    def postprocessing(self, input_data):
        # Interpreting result
        label = "Normal"
        if input_data[0] < 1:
            label = "Anomaly"
            input_data[0] = -1
        return {"probability": input_data[0], "label": label, "status": "OK"}

    def save_data(self, saved_data, pred):
        # Save data for train again later
        DatosMovimiento.objects.create(acc_x=saved_data['acc_x'], acc_y=saved_data['acc_y'],
                                       acc_z=saved_data['acc_z'], gyr_x=saved_data["gyr_x"],
                                       gyr_y=saved_data["gyr_y"], gyr_z=saved_data["gyr_z"],
                                       fecha=saved_data['fecha'], hora=saved_data['hora'],
                                       anomalia=bool(pred)).save()

    def compute_prediction(self, input_data):
        try:
            input_data, to_save_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)
            prediction = self.postprocessing(prediction)
            self.save_data(to_save_data.loc[1], prediction['probability'])
            self.save_data(to_save_data.loc[2], prediction['probability'])
            print(str(prediction), file=sys.stderr)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction