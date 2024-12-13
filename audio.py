import speech_recognition as sr

def transcribe_audio(file_path):
        # Inicializa o reconhecedor
    recognizer = sr.Recognizer()

    try:
        # Lê o arquivo de áudio
        with sr.AudioFile(file_path) as source:
            print("Processando o áudio...")
            audio_data = recognizer.record(source)

        # Usa o Google Web Speech API para transcrever
        print("Reconhecendo o texto...")
        text = recognizer.recognize_google(audio_data, language="pt-BR")
        return text
    except sr.UnknownValueError:
        return "Não foi possível entender o áudio."
    except sr.RequestError as e:
        return f"Erro ao acessar o serviço de reconhecimento: {e}"
    except Exception as e:
        return f"Erro inesperado: {e}"  

# Caminho do arquivo de áudio
audio_file = "audi_test.wav"

# Transcreve o áudio
transcribed_text = transcribe_audio(audio_file)
print("Texto transcrito:", transcribed_text)
