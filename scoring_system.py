# ============================================================
# MODULE 6: scoring_system.py
# PURPOSE: Combine all individual scores into a Final Score /100
#          and give a performance grade + feedback message
# ============================================================

# -------------------------------------------------------
# SCORE WEIGHTS (must add up to 100)
# -------------------------------------------------------
# Answer Quality:   40 points  (based on keywords & content)
# Emotion:          20 points  (confidence/presence on camera)
# Voice Analysis:   20 points  (speed, clarity, no fillers)
# Bonus:            20 points  (split: 10 fluency + 10 preparation)
# -------------------------------------------------------

def calculate_final_score(answer_score, emotion_score, voice_score, bonus_score=None):
    """
    Combines all module scores into a final score out of 100.

    Parameters:
        answer_score (int): Score from answer_evaluation.py  (max 40)
        emotion_score (int): Score from emotion_detection.py  (max 20)
        voice_score (int): Score from voice_analysis.py        (max 20)
        bonus_score (int): Optional extra points               (max 20)

    Returns:
        (int) final_score out of 100
        (str) grade letter
        (str) feedback message
    """

    # --- Clamp each score to its maximum ---
    answer_score  = max(0, min(answer_score, 40))
    emotion_score = max(0, min(emotion_score, 20))
    voice_score   = max(0, min(voice_score, 20))

    # --- Bonus score ---
    if bonus_score is None:
        # Auto-calculate a small bonus based on overall performance
        avg = (answer_score/40 + emotion_score/20 + voice_score/20) / 3
        bonus_score = int(avg * 20)  # Scale to 20
    bonus_score = max(0, min(bonus_score, 20))

    # --- Final score ---
    final_score = answer_score + emotion_score + voice_score + bonus_score
    final_score = min(final_score, 100)  # Cap at 100

    # --- Grade ---
    grade = _get_grade(final_score)

    # --- Feedback ---
    feedback = _get_feedback(final_score, answer_score, emotion_score, voice_score)

    return final_score, grade, feedback


def _get_grade(score):
    """
    Convert numeric score to a letter grade.
    """
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"


def _get_feedback(final, answer, emotion, voice):
    """
    Generate personalized feedback based on the scores.
    """
    messages = []

    # Answer feedback
    if answer >= 30:
        messages.append("✅ Great answer content! You covered the key points well.")
    elif answer >= 20:
        messages.append("📝 Decent answer. Try to include more technical keywords.")
    else:
        messages.append("📝 Work on your answer content — practice common interview questions.")

    # Emotion feedback
    if emotion >= 15:
        messages.append("😊 You appeared confident and engaged on camera.")
    elif emotion >= 10:
        messages.append("🙂 Try to maintain eye contact and sit up straight.")
    else:
        messages.append("📷 Make sure your face is clearly visible and you appear calm.")

    # Voice feedback
    if voice >= 15:
        messages.append("🔊 Excellent speaking pace and clarity!")
    elif voice >= 10:
        messages.append("🗣️  Good effort. Try to reduce filler words like 'um' and 'uh'.")
    else:
        messages.append("🗣️  Practice speaking at a steady, clear pace for interviews.")

    return "\n   ".join(messages)


def print_final_report(question, answer_text, answer_score, emotion, emotion_score, voice_score, final_score, grade, feedback):
    """
    Print a beautiful final report to the terminal.
    """
    print("\n")
    print("=" * 55)
    print("         🏆  AI INTERVIEW ANALYZER — RESULTS  🏆")
    print("=" * 55)
    print(f"  Question:        {question[:60]}...")
    print(f"  Your Answer:     {answer_text[:60]}...")
    print("-" * 55)
    print(f"  📝 Answer Score:   {answer_score}/40")
    print(f"  😊 Emotion:        {emotion}  ({emotion_score}/20)")
    print(f"  🔊 Voice Score:    {voice_score}/20")
    print("-" * 55)
    print(f"  🏅 FINAL SCORE:    {final_score}/100   Grade: {grade}")
    print("=" * 55)
    print("\n  📋 Feedback:")
    print(f"   {feedback}")
    print("=" * 55)
    print()


# ---- Quick Test ----
if __name__ == "__main__":
    score, grade, feedback = calculate_final_score(
        answer_score=30,
        emotion_score=15,
        voice_score=14
    )
    print(f"Final Score: {score}/100 | Grade: {grade}")
    print(f"Feedback:\n{feedback}")
