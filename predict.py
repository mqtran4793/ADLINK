import numpy as np
import tensorflow as tf
import cv2
from tensorflow import keras
from keras.utils import np_utils
from keras.preprocessing.image import load_img
from keras import backend as K

K.set_learning_phase(0)

new_model = keras.models.load_model('saved_model/handwritten_digits_detection_model.h5')
#new_model.summary()

def freeze_session(session, keep_var_names=None, output_names=None, clear_devices=True):
    #from tensorflow.python.framework.graph_util import convert_variables_to_constants

    graph = session.graph
    with graph.as_default():
        freeze_var_names = list(set(v.op.name for v in tf.global_variables()).difference(keep_var_names or []))
        output_names = output_names or []
        output_names += [v.op.name for v in tf.global_variables()]
        # Graph -> GraphDef ProtoBuf
        input_graph_def = graph.as_graph_def()
        if clear_devices:
            for node in input_graph_def.node:
                node.device = ""
        frozen_graph = tf.compat.v1.graph_util.convert_variables_to_constants(session, input_graph_def,
                                                      output_names, freeze_var_names)
        return frozen_graph


frozen_graph = freeze_session(K.get_session(),
                              output_names=[out.op.name for out in new_model.outputs])

tf.io.write_graph(frozen_graph, "model", "saved_model.pb", as_text=False)


"""
img = []
for i in range(20):
    path = '/home/adlink/Desktop/' + str(i) + '.jpg'
    img.append(cv2.imread(path))

for i in img:
    i = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
    #i = cv2.bitwise_not(i)

    cv2.imshow('Image', i)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    i = cv2.resize(i, (28, 28))
    i = np.reshape(i, [1, 28, 28, 1])
    i = i.astype('float32')
    i = i / 255.0

    print(new_model.predict(i))
    print('Predicted label: ', new_model.predict_classes(i))
    print('\n')

tf.saved_model.save(new_model, '/home/adlink/DeepLearning/model')
"""
"""
print('\n')
print(new_model.outputs)
print(new_model.inputs)
"""