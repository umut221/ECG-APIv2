from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import heartpy as hp
import csv
import numpy as np
import math

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

class CSVReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.current_index = 0
        self.chunk_size = 12

    def read_data(self):
        data = []
        with open(self.file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                if i >= self.current_index and i < self.current_index + self.chunk_size:
                    data.extend(row)
        self.current_index += self.chunk_size
        if len(data) < self.current_index:
            self.current_index = 0

        return data

csv_reader = CSVReader('mitbih_test.csv')

def get_data():
    data = list(csv_reader.read_data())
    data = np.array(data, dtype=float)
    return data


@app.route('/')
@cross_origin()
def sendData():
    data = get_data()
    listData = list(data)
    return make_response(jsonify(listData))

@app.route('/analyze')
def sendAnalyze():
    data = analyzeData()
    return make_response(jsonify(data))

def analyzeData():
  data = get_data()
  working_data, measures = hp.process(data,150.0)
  cleaned_data = {key: value for key, value in measures.items() if not math.isnan(value)}
  wd, m = hp.analysis.calc_fd_measures(method = 'periodogram', measures = cleaned_data, working_data = working_data)
  return m


if __name__ == '__main__':
    app.run(debug=True)
