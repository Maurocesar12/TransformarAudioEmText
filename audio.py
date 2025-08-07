import streamlit as st
from pydub import AudioSegment
import speech_recognition as sr
import tempfile
import os

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language="pt-BR")
        return text
    except sr.UnknownValueError:
        return "Não foi possível entender o áudio."
    except sr.RequestError as e:
        return f"Erro ao acessar o serviço de reconhecimento: {e}"
    except Exception as e:
        return f"Erro inesperado: {e}"

st.set_page_config(page_title="Transcrição de Áudio", layout="centered")
st.title("🎙️ Transcrição de Áudio para Texto")

uploaded_file = st.file_uploader("Envie seu arquivo de áudio", type=["wav", "mp3", "m4a", "ogg"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_input:
        tmp_input.write(uploaded_file.read())
        tmp_input.flush()

        # Converter o áudio usando pydub
        audio = AudioSegment.from_file(tmp_input.name)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
            audio.export(tmp_wav.name, format="wav")
            tmp_wav_path = tmp_wav.name

            # Transcrição
            texto = transcribe_audio(tmp_wav_path)

            # Exibir resultado
            st.success("✅ Transcrição concluída!")
            st.text_area("Texto transcrito:", texto, height=200)

            # Apagar com segurança
            try:
                os.remove(tmp_wav_path)
            except PermissionError:
                st.warning("⚠️ Arquivo temporário ainda em uso, tente novamente mais tarde.")
