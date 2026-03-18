# ============================================================
# MODULE 1: voice_questions.py
# PURPOSE: Ask interview questions using Text-to-Speech (TTS)
#          Falls back to print() if TTS is not available
# ============================================================

import time

# List of interview questions
INTERVIEW_QUESTIONS = [
    "What is Artificial Intelligence? Explain in your own words.",
    "Can you describe a project you have worked on recently?",
    "What are your strengths and weaknesses?",
    "Where do you see yourself in five years?",
    "Why do you want this job?"
]

def speak_question(text):
    """
    Try to speak the question using pyttsx3 (Text-to-Speech).
    If pyttsx3 is not installed, just print the question instead.
    """
    try:
        import pyttsx3
        engine = pyttsx3.init()           # Start the TTS engine
        engine.setProperty('rate', 150)   # Set speaking speed (words per minute)
        engine.setProperty('volume', 1.0) # Set volume (0.0 to 1.0)
        engine.say(text)                  # Queue the text to speak
        engine.runAndWait()               # Wait until speaking is done
    except ImportError:
        # pyttsx3 not installed — just print the question
        print(f"\n🎤 QUESTION: {text}")
    except Exception as e:
        # Any other error — fall back to printing
        print(f"\n🎤 QUESTION: {text}")
        print(f"   (TTS Error: {e})")

def get_question(index=0):
    """
    Return a question from the list by index.
    If index is out of range, return the first question.
    """
    if 0 <= index < len(INTERVIEW_QUESTIONS):
        return INTERVIEW_QUESTIONS[index]
    return INTERVIEW_QUESTIONS[0]

def ask_question(index=0):
    """
    Main function: Get a question, print it, and speak it.
    Returns the question text so other modules can use it.
    """
    question = get_question(index)
    print("\n" + "="*50)
    print(f"📌 Question {index + 1}: {question}")
    print("="*50)
    speak_question(question)
    time.sleep(1)  # Small pause after speaking
    return question


# ---- Quick Test ----
if __name__ == "__main__":
    asked = ask_question(0)
    print(f"\n[Test] Question returned: {asked}")
