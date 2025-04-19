# from core import Tess
# from core.automation.executor import run_with_retry_and_reflection
# import speech_recognition as sr
# import pyttsx3
# # 🗣️ Setup TTS engine
# engine = pyttsx3.init()
# engine.setProperty('rate', 180)  # speed (words per min)
# engine.setProperty('volume', 1.0)  # max volume

# def speak(text):
#     print(f"Tess: {text}")
#     engine.say(text)
#     engine.runAndWait()

# def get_user_input():
#     r = sr.Recognizer()
#     r.energy_threshold = 300
#     try:
#         mic = sr.Microphone()
#         with mic as source:
#             print("🎤 Listening... (or press Enter to type)")
#             audio = r.listen(source, timeout=5, phrase_time_limit=10)
#             print("🧠 Transcribing...")
#             text = r.recognize_google(audio)
#             print(f"You (voice): {text}")
#             return text
#     except Exception as e:
#         print(f"(STT failed: {e})")
#         return input("You (typed): ").strip()


# Tess.run_boot_diagnostics()
# print("\U0001F9E0 Tess is ready. Say something or type. Say 'exit' to quit.\n")

# while True:
#     user_input = get_user_input().strip()

#     if user_input.lower() in ["exit", "quit"]:
#         print("\U0001F44B Bye.")
#         break

#     if user_input.lower().startswith("search "):
#         query = user_input[7:]
#         summary = Tess.search_and_summarize(query)
#         print(f"Tess: {summary}\n")
#         continue

#     if any(x in user_input.lower() for x in ["check", "run", "list", "open", "show", "display"]):
#         cmds = Tess.extract_commands(user_input)
#         for cmd in cmds:
#             print(f"\n🧠 Running: {cmd}")
#             result = run_with_retry_and_reflection(cmd)

#             if result["success"]:
#                 print(f"✅ Output:\n{result['output']}\n")
#             else:
#                 print(f"❌ Final failure:\n{result['output']}\n")
#         continue

#     if user_input.lower().startswith("find "):
#         original_query = user_input[5:].strip()
#         query = Tess.extract_folder_name(original_query)

#         # Let LLM guess where to look
#         guesses = Tess.guess_search_locations(query)
#         folder_path = Tess.smart_find_folder(query, guesses)

#         if folder_path:
#             print(f"✅ Found folder: {folder_path}")
#             cmd = f"open '{folder_path}'"
#             result = run_with_retry_and_reflection(cmd)

#             if result["success"]:
#                 print(f"📟 ✅ Opened: {folder_path}\n")
#             else:
#                 print(f"📟 ❌ Couldn't open: {result['output']}\n")
#         else:
#             print(f"❌ Couldn't locate a folder matching '{query}'\n")
#         continue

#     # Default: memory + RAG fallback
#     Tess.summarize_and_store_if_needed(message=user_input)
#     response = Tess.rag_chain.invoke({"query": user_input})["result"]
#     speak(response + "\n")














# from core import Tess
# from core.automation.executor import run_with_retry_and_reflection
# import speech_recognition as sr
# import pyttsx3
# import argparse
# import platform

# # 🛠️ Command-line flags
# parser = argparse.ArgumentParser()
# parser.add_argument("--no-voice", action="store_true", help="Disable TTS output")
# args = parser.parse_args()
# mute_mode = args.no_voice

# # 🗣️ Setup TTS engine
# engine = pyttsx3.init()
# engine.setProperty('rate', 180)
# engine.setProperty('volume', 1.0)

# # Try to find a female-sounding voice
# voice_found = False
# for voice in engine.getProperty('voices'):
#     if "female" in voice.name.lower() or "samantha" in voice.name.lower() or "zira" in voice.name.lower():
#         engine.setProperty('voice', voice.id)
#         voice_found = True
#         break

# if not voice_found:
#     print("⚠️ No female voice found. Using default.")

# # 🔊 Say something
# def speak(text):
#     print(f"Tess: {text}")
#     if not mute_mode:
#         engine.say(text)
#         engine.runAndWait()

# # 🎤 Listen for user input
# def get_user_input():
#     if mute_mode:
#         return input("You (typed): ").strip()

#     r = sr.Recognizer()
#     r.energy_threshold = 300
#     try:
#         mic = sr.Microphone()
#         with mic as source:
#             print("🎤 Listening... (or press Enter to type)")
#             audio = r.listen(source, timeout=5, phrase_time_limit=10)
#             print("🧠 Transcribing...")
#             text = r.recognize_google(audio)
#             print(f"You (voice): {text}")
#             return text
#     except Exception as e:
#         print(f"(STT failed: {e})")
#         return input("You (typed): ").strip()


# # 🚀 Boot
# Tess.run_boot_diagnostics()
# print("\U0001F9E0 Tess is ready. Say something or type. Use '--no-voice' to mute. Say 'exit' to quit.\n")

# # 🔁 Main loop
# while True:
#     user_input = get_user_input().strip()

#     if user_input.lower() in ["exit", "quit"]:
#         print("\U0001F44B Bye.")
#         break

#     if user_input.lower().startswith("search "):
#         query = user_input[7:]
#         summary = Tess.search_and_summarize(query)
#         speak(summary + "\n")
#         continue

#     if any(x in user_input.lower() for x in ["check", "run", "list", "open", "show", "display"]):
#         cmds = Tess.extract_commands(user_input)
#         for cmd in cmds:
#             print(f"\n🧠 Running: {cmd}")
#             result = run_with_retry_and_reflection(cmd)
#             speak(result["output"])
#         continue

#     if user_input.lower().startswith("find "):
#         original_query = user_input[5:].strip()
#         query = Tess.extract_folder_name(original_query)

#         guesses = Tess.guess_search_locations(query)
#         folder_path = Tess.smart_find_folder(query, guesses)

#         if folder_path:
#             speak(f"Found folder: {folder_path}")
#             cmd = f"open '{folder_path}'"
#             result = run_with_retry_and_reflection(cmd)
#             speak(result["output"])
#         else:
#             speak(f"Couldn't locate a folder matching {query}")
#         continue

#     # 🧠 Default: memory + RAG fallback
#     Tess.summarize_and_store_if_needed(message=user_input)
#     response = Tess.rag_chain.invoke({"query": user_input})["result"]
#     speak(response + "\n")






from core import Tess
from core.automation.executor import run_with_retry_and_reflection
from module.voice import speak, listen, mute_mode

# 🚀 Boot
Tess.run_boot_diagnostics()
print("\U0001F9E0 Tess is ready. Say something or type. Use '--no-voice' to mute. Say 'exit' to quit.\n")

# 🔁 Main loop
while True:
    user_input = listen().strip()
    if user_input.lower() == "standby":
        enter_standby()
        continue


    if user_input.lower() in ["exit", "quit"]:
        print("\U0001F44B Bye.")
        break

    if user_input.lower().startswith("search "):
        query = user_input[7:]
        summary = Tess.search_and_summarize(query)
        speak(summary + "\n")
        continue

    if any(x in user_input.lower() for x in ["check", "run", "list", "open", "show", "display"]):
        cmds = Tess.extract_commands(user_input)
        for cmd in cmds:
            print(f"\n🧠 Running: {cmd}")
            result = run_with_retry_and_reflection(cmd)
            speak(result["output"])
        continue

    if user_input.lower().startswith("find "):
        original_query = user_input[5:].strip()
        query = Tess.extract_folder_name(original_query)

        guesses = Tess.guess_search_locations(query)
        folder_path = Tess.smart_find_folder(query, guesses)

        if folder_path:
            speak(f"Found folder: {folder_path}")
            cmd = f"open '{folder_path}'"
            result = run_with_retry_and_reflection(cmd)
            speak(result["output"])
        else:
            speak(f"Couldn't locate a folder matching {query}")
        continue

    # 🧠 Default: memory + RAG fallback
    Tess.summarize_and_store_if_needed(message=user_input)
    response = Tess.rag_chain.invoke({"query": user_input})["result"]
    speak(response + "\n")
