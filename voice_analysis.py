# ============================================================
# MODULE 5: voice_analysis.py
# PURPOSE: Analyze the candidate's speech for confidence signals
#          Measures: speaking speed, filler words, answer length
# ============================================================

import time

# -------------------------------------------------------
# SCORING WEIGHTS (out of 20 total)
# -------------------------------------------------------
MAX_VOICE_SCORE = 20

def analyze_voice(transcribed_text, speaking_duration_seconds=None):
    """
    Analyzes the transcribed text and speaking time to estimate:
    - Speaking speed (words per minute)
    - Use of filler words (um, uh, like, etc.)
    - Answer completeness

    Returns:
        (int)  Confidence score out of 20
        (dict) Detailed breakdown of the analysis
    """

    if not transcribed_text or transcribed_text.startswith("["):
        print("⚠️  No valid speech to analyze. Voice Score: 0")
        return 0, {}

    # ---- Step 1: Count words ----
    words = transcribed_text.lower().split()
    word_count = len(words)

    # ---- Step 2: Calculate speaking speed ----
    if speaking_duration_seconds and speaking_duration_seconds > 0:
        # Words Per Minute = (word count / seconds) * 60
        wpm = (word_count / speaking_duration_seconds) * 60
    else:
        # Estimate: assume average speaking time of 1 word per 0.5 sec
        wpm = word_count * 2  # Rough estimate

    # ---- Step 3: Count filler words ----
    filler_words = ["um", "uh", "like", "you know", "basically", "literally",
                    "actually", "so", "right", "okay", "hmm", "err"]
    filler_count = sum(words.count(fw) for fw in filler_words)

    # ---- Step 4: Calculate each sub-score ----

    # Speed score (ideal: 120–160 WPM for interviews)
    speed_score = _score_speaking_speed(wpm)

    # Filler word penalty
    filler_score = _score_filler_words(filler_count, word_count)

    # Length score (more complete answers = better)
    length_score = _score_answer_length(word_count)

    # ---- Total voice score ----
    total = speed_score + filler_score + length_score
    final_score = min(total, MAX_VOICE_SCORE)  # Cap at 20

    analysis = {
        "word_count": word_count,
        "words_per_minute": round(wpm),
        "filler_words_found": filler_count,
        "speed_score": speed_score,
        "filler_score": filler_score,
        "length_score": length_score
    }

    print(f"\n🔊 Voice Analysis:")
    print(f"   Word Count:         {word_count} words")
    print(f"   Est. Speaking Speed:{round(wpm)} WPM")
    print(f"   Filler Words Found: {filler_count}")
    print(f"   Speed Score:        {speed_score}/8")
    print(f"   Filler Score:       {filler_score}/6")
    print(f"   Length Score:       {length_score}/6")
    print(f"   Voice/Confidence:   {final_score}/{MAX_VOICE_SCORE}")

    return final_score, analysis


def _score_speaking_speed(wpm):
    """
    Score based on speaking speed.
    Ideal interview speed: 120–160 WPM
    Too slow (<80): appears hesitant
    Too fast (>200): hard to follow
    """
    if 120 <= wpm <= 160:
        return 8    # Perfect speed
    elif 90 <= wpm < 120 or 160 < wpm <= 180:
        return 6    # Slightly off but acceptable
    elif 70 <= wpm < 90 or 180 < wpm <= 200:
        return 4    # Noticeably slow or fast
    else:
        return 2    # Too slow or too fast


def _score_filler_words(filler_count, word_count):
    """
    Score based on filler word usage.
    Fewer fillers = more confident speaker.
    """
    if word_count == 0:
        return 0

    filler_ratio = filler_count / word_count

    if filler_ratio == 0:
        return 6    # No fillers — excellent!
    elif filler_ratio < 0.05:
        return 5    # Very few fillers
    elif filler_ratio < 0.10:
        return 3    # Some fillers
    else:
        return 1    # Too many fillers


def _score_answer_length(word_count):
    """
    Score based on answer completeness.
    Ideal: 20–80 words for a spoken answer.
    """
    if word_count >= 30:
        return 6    # Detailed answer
    elif word_count >= 15:
        return 4    # Decent length
    elif word_count >= 5:
        return 2    # Too short
    else:
        return 0    # Almost nothing said


# ---- Quick Test ----
if __name__ == "__main__":
    test_text = "Artificial intelligence is basically the simulation of human intelligence in computers and machines that learn from data and improve over time"
    score, details = analyze_voice(test_text, speaking_duration_seconds=10)
    print(f"\n[Test] Voice Score: {score}/20")
    print(f"[Test] Details: {details}")
