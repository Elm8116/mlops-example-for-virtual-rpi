import os
from flask import Flask, request, send_from_directory, render_template
import tflite_runtime.interpreter as tflite
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename
import time


ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
IMAGE_SIZE = (224, 224)
UPLOAD_FOLDER = 'uploads'
input_mean = 127.5
input_std = 127.5


def load_labels(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]


# load model and allocate tensors
def load_model(model_path):
    armnn_delegate = tflite.load_delegate('./libarmnnDelegate.so.25',
                                          options={
                                              "backends": "CpuAcc, CpuRef, GpuAcc ",
                                              "logging-severity": "info"
                                          }
                                          )
    model = tflite.Interpreter(model_path, experimental_delegates=[armnn_delegate])
    model.allocate_tensors()

    return model


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def predict(file):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    floating_model = input_details[0]['dtype'] == np.float32

    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    img = Image.open(file).resize((width, height))
    # add N dim
    input_data = np.expand_dims(img, axis=0)

    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()
    start_time = time.time()
    interpreter.invoke()
    stop_time = time.time()
    time_ms = round((stop_time-start_time) * 1000, 2)

    output_data = interpreter.get_tensor(output_details[0]['index'])
    results = np.squeeze(output_data)

    top_k = results.argsort()[-5:][::-1]
    labels = load_labels('labels.txt')
    if floating_model:
        return labels[top_k[0]], time_ms
    else:
        return labels[top_k[0]], time_ms


App = Flask(__name__)
App.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@App.route("/")
def template_test():
    return render_template('home.html', label='', imagesource='file://null')


@App.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(App.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            output, inference_time = predict(file_path)
    return render_template("home.html", label=output, label_=inference_time, imagesource=file_path)


@App.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(App.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == "__main__":

    interpreter = load_model('mobilenet_v1_1.0_224_quant.tflite')
    port = int(os.environ.get('PORT', 8080))
    App.run(debug=False, host='0.0.0.0', port=port)
