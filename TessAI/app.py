# from core.llm import llm
# from core.memory import rag_chain, summarize_and_store_if_needed
# from core.search import search_and_summarize
# import time, os
# from tqdm import tqdm
# from tests import test_boot
# from core.automation.terminal import run_in_new_terminal
# from core.automation.command_planner import extract_commands
# from core.automation.terminal import run_in_new_terminal
# from core.automation.explorer import find_folder, trace_find_folder



# def run_boot_diagnostics():
#     print("🚀 Running system checks...\n")
#     checks = [
#         ("Testing LLM response...", test_boot.test_llm_response),
#         ("Testing memory quality...", test_boot.test_memory_summary_filter),
#     ]

#     for i, (desc, func) in enumerate(checks):
#         time.sleep(0.4)
#         tqdm.write(f"[{'#' * ((i+1)*3)}{'-' * (10 - (i+1)*3)}] {int((i+1)/len(checks)*100)}% {desc}", end=' ')
#         passed = func()
#         tqdm.write("✔ PASS" if passed else "❌ FAIL")

#     print("\n✅ All tests passed.\n")
#     print("(Launching Tess in 2 seconds...)")
#     time.sleep(2)
#     os.system("clear")

# run_boot_diagnostics()
# print("🧠 Tess is ready. Type 'exit' to quit.\n")

# while True:
#     user_input = input("You: ").strip()

#     if user_input.lower() in ["exit", "quit"]:
#         print("👋 Bye.")
#         break
    

#     if user_input.lower().startswith("search "):
#         query = user_input[7:]
#         summary = search_and_summarize(query)
#         print(f"Tess: {summary}\n")
#         continue


#     # Detect natural run request
#     if any(x in user_input.lower() for x in ["check", "run", "list", "open", "show", "display"]):
#         cmds = extract_commands(user_input)
#         for cmd in cmds:
#             output = run_in_new_terminal(cmd)
#             print(f"📟 {output}")
#         continue

#     if "find" in user_input.lower() and "folder" in user_input.lower():
#         query = user_input.lower().split("find")[-1].strip()
#         folder = find_folder(query)
#         if folder:
#             print(f"✅ Found folder: {folder}")
#             output = run_in_new_terminal(f"ls -la '{folder}'")
#             print(f"\n📟 {output}\n")
#         else:
#             print(f"❌ Couldn't locate a folder matching '{query}'\n")
#         continue




#     summarize_and_store_if_needed(user_input)
#     response = rag_chain.invoke({"query": user_input})["result"]
#     print(f"Tess: {response}\n")








from core import Tess

Tess.run_boot_diagnostics()
print("\U0001F9E0 Tess is ready. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ["exit", "quit"]:
        print("\U0001F44B Bye.")
        break

    if user_input.lower().startswith("search "):
        query = user_input[7:]
        summary = Tess.search_and_summarize(query)
        print(f"Tess: {summary}\n")
        continue

    if any(x in user_input.lower() for x in ["check", "run", "list", "open", "show", "display"]):
        cmds = Tess.extract_commands(user_input)
        for cmd in cmds:
            output = Tess.run_in_terminal(cmd)
            print(f"\U0001F4DF {output}")
        continue

    if user_input.lower().startswith("find "):
        original_query = user_input[5:].strip()
        query = Tess.extract_folder_name(original_query)


        # Let LLM guess where to look
        guesses = Tess.guess_search_locations(query)
        folder_path = Tess.smart_find_folder(query, guesses)

        if folder_path:
            print(f"✅ Found folder: {folder_path}")
            cmd = f"open '{folder_path}'"  # or ls -la '{folder_path}' if you want terminal listing
            output = Tess.run_in_new_terminal(cmd)
            print(f"\n📟 {output}\n")
        else:
            print(f"❌ Couldn't locate a folder matching '{query}'\n")
        continue


    Tess.summarize_and_store_if_needed(message=user_input)
    response = Tess.rag_chain.invoke({"query": user_input})["result"]
    print(f"Tess: {response}\n")
