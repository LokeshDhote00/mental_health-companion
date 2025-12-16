# import cohere

# co = cohere.Client("03CDkzZOYPcR0tmnfRaKR1BuZxcNdjbQjUKTx1ET")

# system_prompt = (
#     "SYSTEM: You are a personal health and habit coach AI. "
#     "Generate a personalized daily plan for the user based on the given data. "
#     "Keep it practical, beginner-friendly, suitable for Indian users, and mood-adjusted. "
#     "Always format bullet points each on a new line for clarity.\n"
#     "and if user normally talks then give short and precise answers of single line"
# )

# def ai_response(user_message):
#     full_prompt = system_prompt + "USER: " + user_message

#     response = co.chat(
#         model="command-a-03-2025",
#         message=full_prompt,
#         temperature=0.4
#     )
#     return response.text.strip()
# import cohere

# co = cohere.Client("03CDkzZOYPcR0tmnfRaKR1BuZxcNdjbQjUKTx1ET")

# health_keywords = [
#     "fever", "cold", "cough", "pain", "stress", "anxiety", "sad",
#     "sleep", "headache", "diet", "tired", "weakness", "health",
#     "mental", "doctor", "medicine", "medical"
# ]

# system_prompt = """
# You are a personal mental–health and wellness companion for Indian users.
# Your behavior depends on user intent:

# 1) If the message is a HEALTH ISSUE:
#    - Give a structured daily plan.
#    - Write in bullet points.
#    - New line for every point.
#    - Be empathetic, practical and beginner-friendly.

# 2) If message is NORMAL TALK:
#    - Give a SHORT, friendly reply.
#    - Max 1–2 lines.
#    - No daily plan.
#    - Act like a casual companion.

# Always maintain a caring tone.
# """

# def is_health_query(text):
#     text = text.lower()
#     return any(word in text for word in health_keywords)

# def ai_response(user_message):
#     mode = "health" if is_health_query(user_message) else "normal"

#     if mode == "normal":
#         prompt = (
#             system_prompt +
#             "\nUser intent: NORMAL TALK\nUser: " + user_message +
#             "\nGive a short 1–2 line friendly reply only."
#         )
#     else:
#         prompt = (
#             system_prompt +
#             "\nUser intent: HEALTH ISSUE\nUser: " + user_message +
#             "\nGive a detailed daily plan in bullet points."
#         )

#     response = co.chat(
#         model="command-a-03-2025",
#         message=prompt,
#         temperature=0.4
#     )

#     return response.text.strip()

# import cohere

# co = cohere.Client("03CDkzZOYPcR0tmnfRaKR1BuZxcNdjbQjUKTx1ET")

# # -------------------------
# # MESSAGE CLASSIFIER
# # -------------------------

# def classify_message(message):

#     msg = message.lower()

#     # 1️⃣ If user explicitly asks for medicine → SHORT
#     medicine_verbs = ["medicine", "tablet", "dose", "dawa", "tablet bataye", "medicine batao"]
#     for w in medicine_verbs:
#         if w in msg:
#             return "medicine_short"

#     # 2️⃣ General health symptoms → FULL PLAN
#     medical_keywords = [
#         "fever", "cough", "cold", "pain", "headache", "injury",
#         "stress", "anxiety", "health", "symptom", "doctor", "treatment"
#     ]

#     for w in medical_keywords:
#         if w in msg:
#             return "medical_plan"

#     # 3️⃣ Otherwise normal chat
#     return "normal"


# # -------------------------
# # AI RESPONSE GENERATOR
# # -------------------------

# def generate_ai(message, mode):

#     # ---------------------- CASE 1: SHORT MEDICINE REPLY ----------------------
#     if mode == "medicine_short":
#         prompt = (
#             "You are a friendly Indian health helper.\n"
#             "User is specifically asking for MEDICINE advice.\n"
#             "Give a SHORT 1–2 line reply.\n"
#             "No daily plan.\n"
#             f"User: {message}"
#         )

#     # ---------------------- CASE 2: FULL HEALTH PLAN ----------------------
#     elif mode == "medical_plan":
#         prompt = (
#             "SYSTEM: You are a personal health and habit coach AI.\n"
#             "User has a health issue. Give a structured daily plan.\n"
#             "- Use bullet points\n"
#             "- Each point on new line\n"
#             "- Indian lifestyle based\n"
#             "- Beginner friendly\n\n"
#             f"User: {message}\n"
#         )

#     # ---------------------- CASE 3: NORMAL CHAT ----------------------
#     else:
#         prompt = (
#             "You are a friendly Indian chatbot.\n"
#             "Give a short, casual 1–2 line reply.\n"
#             f"User: {message}"
#         )

#     response = co.chat(
#         model="command-a-03-2025",
#         message=prompt,
#         temperature=0.4
#     )

#     return response.text.strip()
import cohere

co = cohere.Client("03CDkzZOYPcR0tmnfRaKR1BuZxcNdjbQjUKTx1ET")

health_keywords = [
    "fever", "cold", "cough", "pain", "stress", "anxiety", "sad",
    "sleep", "headache", "diet", "tired", "weakness", "health",
    "mental", "doctor", "medicine", "medical"
]

system_prompt = """
You are a personal mental–health and wellness companion for Indian users.
Your behavior depends on user intent:

1) If the message is a HEALTH ISSUE:
   - Give a structured daily plan.
   - Write in bullet points.
   - New line for every point.
   - Be empathetic, practical and beginner-friendly.

2) If message is NORMAL TALK:
   - Give a SHORT, friendly reply.
   - Max 1–2 lines.
   - No daily plan.
   - Act like a casual companion.

Always maintain a caring tone.
"""

def classify_message(text):
    text = text.lower()
    return "health" if any(word in text for word in health_keywords) else "normal"

def generate_ai(user_message, mode):
    if mode == "normal":
        prompt = (
            system_prompt +
            "\nUser intent: NORMAL TALK\nUser: " + user_message +
            "\nGive a short 1–2 line friendly reply only."
        )
    else:
        prompt = (
            system_prompt +
            "\nUser intent: HEALTH ISSUE\nUser: " + user_message +
            "\nGive a detailed daily plan in bullet points."
        )

    response = co.chat(
        model="command-a-03-2025",
        message=prompt,
        temperature=0.4
    )

    return response.text.strip()
