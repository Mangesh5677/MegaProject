from gtts import gTTS


def speak(text):

    filename = "voice.mp3"

    tts = gTTS(
        text=text,
        lang="en"
    )

    tts.save(filename)

    return filename