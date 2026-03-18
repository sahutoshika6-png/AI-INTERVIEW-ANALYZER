# ============================================================
# MODULE 2: speech_to_text.py
# PURPOSE: Record audio from microphone and convert to text
#          Uses SpeechRecognition library (free & beginner-friendly)
# ============================================================

import speech_recognition as sr  # Main library for speech recognition

def record_and_transcribe(duration=8):
    """
    Records audio from the microphone for `duration` seconds,
    then converts it to text using Google's free Speech API.

    Returns:
        (str) The transcribed text, or an error message string.
    """
    recognizer = sr.Recognizer()  # Create a recognizer object

    print(f"\n🎙️  Microphone is ON. Speak now... (up to {duration} seconds)")
    print("   (Tip: Speak clearly and not too fast)\n")

    try:
        # Use the default microphone as audio source
        with sr.Microphone() as source:
            # Adjust for background noise (takes ~1 second)
            recognizer.adjust_for_ambient_noise(source, duration=1)

            # Record audio — waits up to `duration` seconds
            audio = recognizer.listen(source, timeout=duration, phrase_time_limit=duration)

        print("⏳ Processing your speech...")

        # Send audio to Google's free speech-to-text API
        text = recognizer.recognize_google(audio)
        print(f"✅ Transcribed Text: \"{text}\"")
        return text

    except sr.WaitTimeoutError:
        # No speech detected within the timeout period
        msg = "[No speech detected. Please speak louder or sooner.]"
        print(f"⚠️  {msg}")
        return msg

    except sr.UnknownValueError:
        # Audio was recorded but couldn't be understood
        msg = "[Could not understand the audio. Please speak more clearly.]"
        print(f"⚠️  {msg}")
        return msg

    except sr.RequestError as e:
        # API call failed (e.g., no internet connection)
        msg = f"[Speech API error: {e}. Check your internet connection.]"
        print(f"❌ {msg}")
        return msg

    except OSError:
        # Microphone not found or not connected
        msg = "[Microphone not found. Using dummy text for testing.]"
        print(f"⚠️  {msg}")
        # Return a dummy answer so the rest of the program still works
        return "Artificial intelligence is the simulation of human intelligence by machines"


def get_dummy_answer():
    """
    Returns a hardcoded test answer.
    Useful for testing without a microphone.
    """
    return "Artificial intelligence is when machines simulate human intelligence and learning"


# ---- Quick Test ----
if __name__ == "__main__":
    result = record_and_transcribe(duration=8)
    print(f"\n[Test] Final transcription: {result}")
