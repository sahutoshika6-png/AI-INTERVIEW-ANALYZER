# ============================================================
# main.py — AI Interview Analyzer
# PURPOSE: Master script that runs the full interview pipeline
#
# PIPELINE:
#   1. Ask a question (voice + text)
#   2. Record your spoken answer
#   3. Convert speech to text
#   4. Evaluate the answer content
#   5. Detect emotion from webcam
#   6. Analyze voice/confidence
#   7. Generate final score
# ============================================================

import sys
import os
import time

# Add the modules folder to Python's path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "modules"))

# Import all our custom modules
from voice_questions   import ask_question
from speech_to_text    import record_and_transcribe
from answer_evaluation import evaluate_answer
from emotion_detection import detect_emotion
from voice_analysis    import analyze_voice
from scoring_system    import calculate_final_score, print_final_report


def run_interview(question_index=0, recording_duration=10):
    """
    Runs a complete AI interview session for ONE question.

    Steps:
        1) Ask question
        2) Record answer
        3) Transcribe speech
        4) Score answer, emotion, voice
        5) Print final report
    """

    print("\n" + "🤖 " * 18)
    print("     WELCOME TO AI INTERVIEW ANALYZER")
    print("🤖 " * 18)
    print("\nThis system will:")
    print("  1. Ask you an interview question")
    print("  2. Record your spoken answer")
    print("  3. Analyze your content, emotion, and voice")
    print("  4. Give you a score out of 100\n")

    input("📌 Press ENTER when you are ready to begin... ")

    # -------------------------------------------------------
    # STEP 1: Ask the question
    # -------------------------------------------------------
    print("\n[STEP 1/6] Asking your interview question...")
    question = ask_question(question_index)

    # Give user time to prepare
    print("\n⏳ You have 3 seconds to prepare your answer...")
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    print("   SPEAK NOW! 🎙️\n")

    # -------------------------------------------------------
    # STEP 2 & 3: Record audio and convert to text
    # -------------------------------------------------------
    print("[STEP 2/6] Recording your answer...")
    transcribed_answer = record_and_transcribe(duration=recording_duration)

    # -------------------------------------------------------
    # STEP 4: Evaluate answer content
    # -------------------------------------------------------
    print("\n[STEP 3/6] Evaluating your answer content...")
    answer_score, found_keywords = evaluate_answer(transcribed_answer, question_index)

    # -------------------------------------------------------
    # STEP 5: Detect emotion from webcam
    # -------------------------------------------------------
    print("\n[STEP 4/6] Detecting emotion from webcam...")
    print("   (A camera window will open — look at it naturally)")
    emotion_label, emotion_score = detect_emotion(capture_duration=5)

    # -------------------------------------------------------
    # STEP 6: Analyze voice confidence
    # -------------------------------------------------------
    print("\n[STEP 5/6] Analyzing your voice patterns...")
    voice_score, voice_details = analyze_voice(
        transcribed_answer,
        speaking_duration_seconds=recording_duration
    )

    # -------------------------------------------------------
    # STEP 7: Calculate final score
    # -------------------------------------------------------
    print("\n[STEP 6/6] Calculating your final score...")
    final_score, grade, feedback = calculate_final_score(
        answer_score=answer_score,
        emotion_score=emotion_score,
        voice_score=voice_score
    )

    # -------------------------------------------------------
    # FINAL: Print the complete results report
    # -------------------------------------------------------
    print_final_report(
        question=question,
        answer_text=transcribed_answer,
        answer_score=answer_score,
        emotion=emotion_label,
        emotion_score=emotion_score,
        voice_score=voice_score,
        final_score=final_score,
        grade=grade,
        feedback=feedback
    )

    return final_score


def run_full_interview(num_questions=3, recording_duration=10):
    """
    Optional: Run multiple questions and average the scores.
    """
    scores = []
    for i in range(num_questions):
        print(f"\n\n{'='*55}")
        print(f"  QUESTION {i+1} of {num_questions}")
        print(f"{'='*55}")
        score = run_interview(question_index=i, recording_duration=recording_duration)
        scores.append(score)

        if i < num_questions - 1:
            input(f"\nPress ENTER for the next question... ")

    # Final average
    avg = sum(scores) // len(scores)
    print(f"\n\n{'='*55}")
    print(f"  🏆 INTERVIEW COMPLETE!")
    print(f"  Scores: {scores}")
    print(f"  Average Final Score: {avg}/100")
    print(f"{'='*55}\n")


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":

    print("\nChoose mode:")
    print("  1 = Single question interview (recommended for beginners)")
    print("  2 = Full 3-question interview")

    try:
        choice = input("\nEnter 1 or 2 (default: 1): ").strip() or "1"
    except KeyboardInterrupt:
        print("\n\nExiting. Goodbye!")
        sys.exit(0)

    if choice == "2":
        run_full_interview(num_questions=3, recording_duration=10)
    else:
        run_interview(question_index=0, recording_duration=10)
