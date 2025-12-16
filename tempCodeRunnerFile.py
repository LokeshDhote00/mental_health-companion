
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
