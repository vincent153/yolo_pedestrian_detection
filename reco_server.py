from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
import json
from yolo import YOLO

model = 'model_data/yolo_person.h5'
classes = 'model_data/person.txt'
yolo = YOLO(model_path=model,classes_path=classes)
app = Flask(__name__)

# route http posts to this method
@app.route('/api/facedetection', methods=['POST'])
def detection():
    r = request
    nparr = np.fromstring(r.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    yolo.detect_cvImage(img)
    #print(yolo.det_res)
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0]),'yolo_res':yolo.det_res}
    
    return Response(response=json.dumps(response), status=200, mimetype="application/json")

if __name__ == '__main__':
    # start flask app
    app.debug = False
    app.run(host="0.0.0.0", port=5000)
