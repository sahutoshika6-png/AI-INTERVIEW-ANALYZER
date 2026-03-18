# ============================================================
# MODULE 3: answer_evaluation.py
# PURPOSE: Score the candidate's transcribed answer
#          Uses keyword matching — no heavy AI needed!
# ============================================================

# -------------------------------------------------------
# KEYWORD BANK
# Each question maps to a list of important keywords.
# The more keywords found in the answer, the higher the score.
# -------------------------------------------------------
QUESTION_KEYWORDS = {
    0: ["artificial intelligence", "machine", "learning", "computer", "simulate",
        "human", "intelligence", "data", "algorithm", "automation", "AI", "robot"],

    1: ["project", "built", "developed", "worked", "team", "technology",
        "application", "system", "problem", "solution", "implemented", "created"],

    2: ["strength", "weakness", "improve", "communication", "teamwork",
        "leadership", "organized", "hardworking", "patient", "detail", "learn"],

    3: ["future", "goal", "career", "grow", "improve", "lead", "contribute",
        "specialist", "manage", "develop", "achieve", "aspire"],

    4: ["passionate", "skills", "experience", "contribute", "company", "grow",
        "opportunity", "learn", "interested", "motivated", "challenge", "fit"]
}

# Maximum score for an answer (out of 40 points)
MAX_ANSWER_SCORE = 40

def evaluate_answer(answer_text, question_index=0):
    """
    Compare the candidate's answer against expected keywords.
    Returns a score between 0 and MAX_ANSWER_SCORE (40).

    How scoring works:
    - Each keyword found = points
    - Points are scaled to fit within 40
    - Longer answers with more keywords score higher
    """

    if not answer_text or answer_text.startswith("["):
        # Empty or error answer (from STT failures)
        print("⚠️  No valid answer to evaluate. Score: 0")
        return 0, []

    # Get the keyword list for this question
    keywords = QUESTION_KEYWORDS.get(question_index, QUESTION_KEYWORDS[0])

    # Convert answer to lowercase for case-insensitive matching
    answer_lower = answer_text.lower()

    # Find which keywords appear in the answer
    found_keywords = [kw for kw in keywords if kw.lower() in answer_lower]

    # Calculate how many keywords were found (percentage)
    match_ratio = len(found_keywords) / len(keywords) if keywords else 0

    # --- BONUS: Reward longer, detailed answers ---
    word_count = len(answer_text.split())
    if word_count >= 30:
        length_bonus = 5   # Long answer bonus
    elif word_count >= 15:
        length_bonus = 3   # Medium answer bonus
    elif word_count >= 5:
        length_bonus = 1   # Short answer bonus
    else:
        length_bonus = 0   # Very short answer

    # Final score = keyword score + length bonus, capped at MAX
    raw_score = int(match_ratio * (MAX_ANSWER_SCORE - 5)) + length_bonus
    final_score = min(raw_score, MAX_ANSWER_SCORE)  # Never exceed 40

    # Print the breakdown for the user
    print(f"\n📊 Answer Evaluation:")
    print(f"   Keywords found: {found_keywords if found_keywords else 'None'}")
    print(f"   Keyword match:  {len(found_keywords)}/{len(keywords)}")
    print(f"   Word count:     {word_count} words (bonus: +{length_bonus})")
    print(f"   Answer Score:   {final_score}/{MAX_ANSWER_SCORE}")

    return final_score, found_keywords


# ---- Quick Test ----
if __name__ == "__main__":
    test_answer = "Artificial intelligence is the simulation of human intelligence in machines that learn from data"
    score, keywords = evaluate_answer(test_answer, question_index=0)
    print(f"\n[Test] Score: {score}, Keywords: {keywords}")
