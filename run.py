import re
from main_graph import multiAgent_debater

def strip_thinking(text: str) -> str:
    # Remove <think>...</think> blocks including everything inside
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return cleaned.strip()

state = {
    'input': '',
    'debate_topics': [],
    'count': 0,
    'arguments': [],
    'judgement': ''
}

print("\n  DEBATE IN PROGRESS...\n")
print("-" * 50)

round_num = 0

for update in multiAgent_debater.stream(state, stream_mode="updates"):
    node_name = list(update.keys())[0]
    node_output = update[node_name]

    if node_name == "organiser":
        topics = node_output.get("debate_topics", [])
        print(f"\n ORGANISER — Round topics assigned:")
        for i, topic in enumerate(topics):
            label = "Debater A" if i == 0 else "Debater B"
            print(f"   {label}: {topic}")

    elif node_name == "debate":
        round_num += 1
        arguments = node_output.get("arguments", [])
        print(f"\n  ROUND {round_num} ARGUMENTS:")
        print("-" * 40)
        for argument in arguments:
            if argument.startswith("Debater_A"):
                clean = strip_thinking(argument.replace("Debater_A:", "").strip())
                print(f"\n DEBATER A:\n{clean}")
            elif argument.startswith("Debater_B"):
                clean = strip_thinking(argument.replace("Debater_B:", "").strip())
                print(f"\n DEBATER B:\n{clean}")
        print("-" * 40)

    elif node_name == "judgement":
        verdict = strip_thinking(node_output.get("judgement", ""))
        print(f"\n JUDGE'S VERDICT\n")
        print("-" * 50)
        print(verdict)
        print("-" * 50)

print("\n Debate complete.")