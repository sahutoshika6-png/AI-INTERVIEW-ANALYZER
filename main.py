print("AI Interview Analyzer")

name = input("Enter your name: ")

print("Hello", name)
print("Question: What is Artificial Intelligence?")

answer = input("Your answer: ")

print("Your answer was:", answer)


print("AI Interview Analyzer")

name = input("Enter your name: ")

print("Question: What is Artificial Intelligence?")
answer = input("Your answer: ")

keywords = ["machine", "learning", "data", "automation"]

score = 0
for word in keywords:
    if word in answer.lower():
        score += 10

print("Answer Score:", score, "/40")