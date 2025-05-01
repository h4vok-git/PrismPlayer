import whisper 

model = whisper.load_model("base") 
def transcribe_video(file_path):
    result = model.transcribe(file_path)
    return result['text'] 