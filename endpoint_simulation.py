from flask import Flask, jsonify

app = Flask(__name__)
data_list = ['file', 
             'fpga',
             'gpu',
             'network',
             'storage',
             'topology']


@app.route('/liqid/api/v2/status/gpu', methods=['GET'])
def gpu_data():
    with open('gpu.json') as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/liqid/api/v2/status/network', methods=['GET'])
def network_data():
    with open('network.json') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/liqid/api/v2/status/storage', methods=['GET'])
def storage_data():
    with open('storage.json') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)