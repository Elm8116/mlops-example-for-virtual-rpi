import os
from flask import Flask, request, send_from_directory, render_template
import tflite_runtime.interpreter as tflite
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename
import tritonclient.http as tritonhttpclient


ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
IMAGE_SIZE = (224, 224)
UPLOAD_FOLDER = 'uploads'
input_mean = 127.5
input_std = 127.5

VERBOSE = False
input_name = 'input'
input_shape = (1, 244, 244, 3)
input_dtype = 'FP32'
output_name = 'MobilenetV1/Predictions/Reshape_1'
model_name = 'tflite_model'
url = 'localhost:8000'
model_version = '1'
label_path = './models/tflite_model/labels.txt'


def load_labels(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def predict(img_path):
    triton_client = tritonhttpclient.InferenceServerClient(url=url, verbose=VERBOSE)
    model_metadata = triton_client.get_model_metadata(model_name=model_name, model_version=model_version)
    model_config = triton_client.get_model_config(model_name=model_name, model_version=model_version)

    height = input_shape[1]
    width = input_shape[2]

    img = Image.open(img_path).resize((width, height))
    # add N dim
    input_data = np.expand_dims(img, axis=0)
    input_data = (np.float32(input_data) - input_mean) / input_std
    input0 = tritonhttpclient.InferInput(input_name, input_shape, input_dtype)
    input0.set_data_from_numpy(input_data, binary_data=False)

    with open(label_path, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    output = tritonhttpclient.InferRequestedOutput(output_name, binary_data=False)

    response = triton_client.infer(model_name, model_version=model_version,
                                   inputs=[input0], outputs=[output])

    logits = response.as_numpy(output_name)
    logits = np.asarray(logits, dtype=np.float32)
    return labels[np.argmax(logits)]


App = Flask(__name__)
App.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@App.route("/")
def template_test():
    return render_template('home.html', imagesource='file://null')


@App.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            img_file_path = os.path.join(App.config['UPLOAD_FOLDER'], filename)
            output = predict(img_file_path)
    return render_template("home.html", imagesource=img_file_path)


@App.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(App.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":

    port = int(os.environ.get('PORT', 8080))
    App.run(debug=False, host='0.0.0.0', port=port)
