from flask import Flask, request
import traceback
import json
import whisper
from pydub import AudioSegment
import base64
import io


# 读取配置文件
with open("config.json", "r", encoding="utf-8") as fp:
    config_dict = json.load(fp=fp)
# 加载模型
model = whisper.load_model(config_dict["model_name"])

app = Flask(__name__)

@app.route('/', methods=["POST"])
def _():
    try:
        bs64_audio = request.form.get("bs64_audio")
        return {"code": 0,
                "text": transcribe_audio(bs64_audio=bs64_audio)}
    except Exception as e:
        return {"code": -1,
                "error_info": f"{repr(e)}\n" \
                              f"{traceback.format_exc()}"}

def transcribe_audio(bs64_audio: str) -> str:
    # Base64 To Audio
    audio_bytes = base64.b64decode(bs64_audio)
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
    audio_segment.export("output.wav", format="wav")

    # Transcribe audio
    return model.transcribe("output.wav")["text"]

app.run()