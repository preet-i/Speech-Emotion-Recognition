import os
import numpy as np
import librosa
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import AudioFileForm
from .models import AudioFile
from tensorflow.keras.models import load_model

# Load your trained model
MODEL_PATH = os.path.join('static', 'emotion_recognition_model.h5')
model = load_model(MODEL_PATH)

def extract_mfcc(file_path):
    y, sr = librosa.load(file_path, duration=3, offset=0.5)
    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
    return mfcc

def predict_emotion(audio_path):
    mfcc = extract_mfcc(audio_path)
    mfcc = np.expand_dims(mfcc, axis=-1)
    mfcc = np.expand_dims(mfcc, axis=0)
    prediction = model.predict(mfcc)
    labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'ps', 'sad']
    return labels[np.argmax(prediction)]

def upload_file(request):
    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = form.save()
            audio_path = os.path.join(settings.MEDIA_ROOT, audio_file.audio.name)
            emotion = predict_emotion(audio_path)
            emoji=""
            if emotion=="disgust":
                emoji="&#129314"
            context={"emotion":emotion,"emoji":emoji}
            return render(request, 'result.html',context)
    else:
        form = AudioFileForm()
    return render(request, 'upload.html', {'form': form})
# feedback/views.py
from django.shortcuts import render, redirect
from .models import Feedback

# predict/views.py
from django.shortcuts import render, redirect
from .models import Feedback

def feedback_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        feedback_text = request.POST.get('message')

        # Create a new Feedback instance and save it
        Feedback.objects.create(name=name, email=email, feedback=feedback_text)

        return redirect('thank_you')

    return render(request, 'feedback.html')

def thank_you_view(request):
    return render(request, 'thank_you.html')


def thank_you(request):
    return render(request, 'thank_you.html')
