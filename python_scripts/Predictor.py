import pandas as pd
import numpy as np
import time as time
import pickle
import socket
import threading
import concurrent.futures
import os
import keras
from keras.models import load_model
import sys
import codecs
from os import walk
import shutil


class Predictor(object):

    def __init__(self, port):
        self.colNames = ["block1", "block2", "isClone", "COMP1", "NOS1", "HVOC1", "HEFF1", "CREF1", "XMET1", "LMET1",
                         "NOA1", "HDIF1", "VDEC1", "EXCT1", "EXCR1", "CAST1",
                         "NAND1", "VREF1", "NOPR1", "MDN1", "NEXP1", "LOOP1", "NBLTRL1", "NCLTRL1", "NNLTRL1",
                         "NNULLTRL1", "NSLTRL1", "COMP2", "NOS2", "HVOC2", "HEFF2", "CREF2",
                         "XMET2", "LMET2", "NOA2", "HDIF2", "VDEC2", "EXCT2", "EXCR2", "CAST2", "NAND2", "VREF2",
                         "NOPR2", "MDN2", "NEXP2", "LOOP2", "NBLTRL2", "NCLTRL2", "NNLTRL2",
                         "NNULLTRL2", "NSLTRL2"]

        self.thread_counter = 0
        self.num_candidates_31 = 0
        self.num_candidates_32 = 0
        self.array_31 = []
        self.array_32 = []
        self.modelfilename_type31 = '/scratch/mondego/local/farima/tensorFlow/experiments/models/trained_model3_best_precision.h5'
        self.loadModel()
        self.output_dir = '/scratch/mondego/local/farima/oreo-artifact/results/predictions/'

        if (not os.path.isdir(self.output_dir)):
            os.makedirs(self.output_dir)
        self.socketHost = "localhost"
        self.socketPort = port
        self.file_type2 = open(
            "{out_dir}/clonepairs_type2_{port}.txt".format(out_dir=self.output_dir, port=self.socketPort), 'w')
        self.clone_pairs = ''
        self.clone_pairs_count = 0
        self.type2_clonepairs_count = 0
        self.files_processed = set()
        self.files_to_consider = []
        self.candidates_dir = "{directory}/{port}".format(
            directory='/scratch/mondego/local/farima/oreo-artifact/results/candidates/',
            port=self.socketPort)
        self.candidateListFile = "{directory}/candidatesList.txt".format(directory=self.candidates_dir)
        self.FINISHED = 0
        self.CONTINUE = 1
        self.BATCH_SIZE_FOR_PREDICTION = 100
        self.CLONE_FILE_SIZE = 10000

    def loadModel(self):
        self.loaded_model_type31 = load_model(self.modelfilename_type31)
        print("models loaded")

    def connect_socket(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((self.socketHost, self.socketPort))
        serversocket.listen(1)  # maximum  1 connection
        self.connection, self.address = serversocket.accept()
        print("Connection accepted")

    def predict_clones(self, array, clone_type):
        try:
            start_process_pred = time.time()
            array_pred = np.array(array)
            # X_test = array_pred[:, [i for i in range(0, 30+27) if i not in [0, 1, 2, 4,4+27,5+27,8+27,13,13+27,14,14+27,16,16+27,23+27]]]
            X_test = array_pred[:, [i for i in range(3, 51)]]
            X_test = X_test.astype(float)
            X1 = X_test[:, [i for i in range(0, 24)]]
            X2 = X_test[:, [i for i in range(24, 48)]]
            # Y_test = array_pred[:, 2].astype(bool)
            if clone_type == '31':
                pred = self.loaded_model_type31.predict([X1, X2], batch_size=self.BATCH_SIZE_FOR_PREDICTION, verbose=0)
                #pred = self.loaded_model_type31.predict([X1, X2])
                # pred = self.loaded_model_type31.predict(X_test, batch_size=self.BATCH_SIZE_FOR_PREDICTION, verbose=0)
                predictions = np.zeros_like(pred)
                index = pred > 0.5
                predictions[index] = 1
            end_process_pred = time.time()
            print("prediction took: {sec} seconds ".format(sec=(end_process_pred - start_process_pred)))
            for i in range(predictions.shape[0]):
                #for reporting clones: use this if condition:
                if predictions[i]:
                #for reporting non-clones: use this condition:
                #if not predictions[i]:
                    self.clone_pairs += (str(array_pred[i][0]) + ',' + str(array_pred[i][1]) + '\n')
                    self.clone_pairs_count += 1
                    if self.clone_pairs_count > 0 and self.clone_pairs_count % self.CLONE_FILE_SIZE == 0:
                        self.writeClonePairs(clone_type)
        except Exception:
            print(sys.exc_info()[0])

    def writeClonePairs(self, clone_type):
        start_process_pred = time.time()
        self.thread_counter += 1
        clone_file_path = "{output_dir}/clonepairs_{threadId}_type_{cloneType}_{port}.txt".format(
            output_dir=self.output_dir,
            threadId=self.thread_counter,
            cloneType=clone_type,
            port=self.socketPort
        )
        with codecs.open(clone_file_path, "w+") as file_clonepair:
            file_clonepair.write(self.clone_pairs)
        # reset the clone_pairs
        self.clone_pairs = ''
        end_process_pred = time.time()
        print("writing to file took: {sec} seconds ".format(sec=(end_process_pred - start_process_pred)))

    def process(self, data):
        if "FINISHED_JOB" in data:
            print("last prediction started")
            self.predict_clones(self.array_31, '31')
            self.writeClonePairs('31')

            print("Reading Finished. Wait for last thread to finish...")
            return self.FINISHED
        data_splitted = data.split('#$#')
        candidate_pairs = data_splitted[1].split('~~')
        if data_splitted[0] == '2':
            self.type2_clonepairs_count += 1
            self.file_type2.write(candidate_pairs[0] + ',' + candidate_pairs[1] + '\n')
        elif data_splitted[0] == '3.1' or data_splitted[0] == '3.2':
            self.array_31.append(candidate_pairs)
            self.num_candidates_31 += 1
            if self.num_candidates_31 % 1000 == 0:
                print("candidates: {c}".format(c=self.num_candidates_31))
            if len(self.array_31) == self.BATCH_SIZE_FOR_PREDICTION:
                print("prediction started")
                self.predict_clones(self.array_31, '31')
                self.array_31 = []
        return self.CONTINUE

    def start(self):
        data = ""
        self.chunkcounter = 0;
        self.linecounter = 0;
        breakOuterLoop = False
        while True:
            if breakOuterLoop:
                break
            self.chunkcounter += 1
            chunk = self.connection.recv(1024 * 1000 * 350 * 1)
            print("chunk received: {c}".format(c=self.chunkcounter))
            chunk = chunk.decode('utf-8')
            if chunk and len(chunk) > 0:
                data = "{d}{c}".format(d=data, c=chunk)
                if "\n" in data:
                    lines = data.split("\n")
                    for index in range(0, len(lines) - 1):
                        self.linecounter += 1
                        if self.process(lines[index]) == 0:
                            breakOuterLoop = True
                            break
                    data = lines[index + 1]
            else:
                break

    def populateCandidateFiles(self):
        self.files_to_consider = []
        try:
            with codecs.open(self.candidateListFile, "r") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    self.files_to_consider.append(line)
        except FileNotFoundError:
            pass  # do nothing.

    def processCandidateFiles(self):
        status = self.CONTINUE
        for filename in self.files_to_consider:
            if filename not in self.files_processed:
                self.files_processed.add(filename)
                status = self.processCandidateFile(filename)
                os.remove(filename)
        return status

    def processCandidateFile(self, filename):
        print("processing file: {f}".format(f=filename))
        self.processed_file_counter += 1
        with codecs.open(filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                self.linecounter += 1
                if self.process(line) == self.FINISHED:
                    return self.FINISHED
        return self.CONTINUE

    def startJob(self):
        self.linecounter = 0;
        status = self.CONTINUE
        self.processed_file_counter = 0
        while status == self.CONTINUE:
            self.populateCandidateFiles()
            print("found {c} candidate files".format(c=len(self.files_to_consider)))
            status = self.processCandidateFiles()


if __name__ == "__main__":
    start_time = time.time()

    # load model
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
        predictor = Predictor(port)
        # predictor.connect_socket()
        predictor.startJob()
        end_time = time.time()
        predictor.file_type2.close()
        print("whole process took: {sec} seconds ".format(sec=(end_time - start_time)))
        print("finished at: " + str(end_time))
        print("total pairs analyzed: " + str(predictor.linecounter))
        print("total files processed: " + str(predictor.processed_file_counter))
        print("total clonepairs: {t}".format(t=predictor.clone_pairs_count + predictor.type2_clonepairs_count))
    else:
        print("please specify port. one of 9900, 9901, 9902, or 9903")

