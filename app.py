from flask import Flask, request, render_template, send_file
import os
import torch
import numpy as np
import cv2
import moviepy.editor as mp
from models.DreamActor_M1.inference import DreamActorInference

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# אתחול מודל DreamActor
model = DreamActorInference()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if 'image' not in request.files or 'audio' not in request.files:
        return 'חסרים קבצים', 400
        
    image = request.files['image']
    audio = request.files['audio']
    
    if image.filename == '' or audio.filename == '':
        return 'לא נבחרו קבצים', 400
    
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    audio_path = os.path.join(UPLOAD_FOLDER, audio.filename)
    output_path = os.path.join(OUTPUT_FOLDER, 'output.mp4')

    # שמירת הקבצים
    image.save(image_path)
    audio.save(audio_path)

    try:
        # טעינת התמונה והאודיו
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        audio_clip = mp.AudioFileClip(audio_path)
        
        # יצירת האנימציה באמצעות DreamActor
        animated_frames = model.animate_image(img, audio_path)
        
        # המרת הפריימים לוידאו
        clip = mp.ImageSequenceClip(animated_frames, fps=24)
        clip = clip.set_audio(audio_clip)
        clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        return send_file(output_path, as_attachment=True)
        
    except Exception as e:
        return f'שגיאה: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=True) 