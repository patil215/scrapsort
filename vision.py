import numpy as np
import tensorflow as tf

class Classifier:
    modelPath = None
    labelPath = None
    sess = None
    softmax_tensor = None

    def __init__(self, modelPath, labelPath):
        self.modelPath = modelPath
        self.labelPath = labelPath
        """Creates a graph from saved GraphDef file and returns a saver."""
        # Creates graph from saved graph_def.pb.
        with tf.gfile.FastGFile(modelPath, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

        self.sess = tf.Session()
        self.softmax_tensor = self.sess.graph.get_tensor_by_name('final_result:0')

    def get_image_labels(self, imagePath):
        answer = None

        if not tf.gfile.Exists(imagePath):
            tf.logging.fatal('File does not exist %s', imagePath)
            return answer

        image_data = tf.gfile.FastGFile(imagePath, 'rb').read()

        predictions = self.sess.run(self.softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)
        top_k = predictions.argsort()[-5:][::-1] # Getting top 5 predictions
        f = open(self.labelPath, 'rb')
        lines = f.readlines()
        labels = [str(w).replace("\n", "") for w in lines]

        answers = []
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            answers.append({"type": human_string, "score" : score.item() })
        return answers
