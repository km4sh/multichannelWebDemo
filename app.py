from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import sys
import base64
import wave
import soundfile as sf
import librosa
import numpy as np
from static.src.FastMNMF import FastMNMF

app =  Flask(__name__)

@app.route('/',  methods=['POST',  'GET'])
def  index():
    return render_template('index.html')

@app.route('/records',  methods=['POST',  'GET'])
def  record():
    if request.method ==  'POST':
        buffer = request.form['upfile_b64']
        audio = base64.b64decode(buffer)[44:]
        with wave.open('record.wav', 'wb') as f:
            f.setnchannels(2)
            f.setframerate(16000)
            f.setsampwidth(2)
            f.writeframesraw(audio)
        app.logger.info('文件存储完成！')
        n_fft = 4096
        n_source = 2
        n_basis = 6
        init_SCM = 'circular'
        n_bit = 32
        n_iteration = 1
        n_mic = 2
        wav, fs = sf.read('record.wav')
        wav = wav.T
        M = min(n_mic, len(wav))
        for m in range(M):
            tmp = librosa.core.stft(wav[m], n_fft=n_fft, hop_length=int(n_fft/4))
            if m == 0:
                spec = np.zeros([tmp.shape[0], tmp.shape[1], M], dtype=np.complex)
            spec[:, :, m] = tmp
        spec += (np.random.rand(spec.shape[0], spec.shape[1], M) + np.random.rand(spec.shape[0], spec.shape[1], M) * 1j) * np.abs(spec).max() * 1e-5
        separater = FastMNMF.FastMNMF(n_source=n_source, n_basis=n_basis, xp=np, init_SCM=init_SCM, n_bit=n_bit, seed=0)
        separater.load_spectrogram(spec)
        separater.file_id = 'demo'
        separater.solve(n_iteration=n_iteration, save_likelihood=False, save_parameter=False, save_wav=False, save_path="./static/fastmnmf/", interval_save_parameter=25)
        return '/static/fastmnmf/'+separater.filename_suffix+'.wav'
    else:
        app.logger.info("好紧张有人点开了这个页面！")
        return  render_template('records.html')

if  __name__  ==  "__main__":
    app.run(debug=True, port=19872)