import json
import os

import numpy as np
import tensorflow as tf


# use cpu
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


class Model:
    def __init__(self, path):
        self.model = tf.keras.models.load_model(path)
        cat_path = os.path.join(path, 'categories.json')
        with open(cat_path, 'r', encoding='utf-8') as f:
            self.categories = json.load(f)

    def predict(self, text):
        text = text.encode('ascii', 'backslashreplace')
        text = np.array([text])
        result = {self.categories[i]: float(r) for i, r in enumerate(self.model.predict(text)[0])}
        return result


if __name__ == '__main__':
    model = Model('model_facs8')
    with open('file.txt', 'r', encoding='utf-8') as f:
        print(model.predict(f.read()))
