from .config import get_llm
from .tools import load_notes, search_notes, calculate


def run_cli():
    """
    Simple command-line "agent":

    - Uses Llama (via Ollama) as the LLM
    - Automatically searches your notes and injects them as context
    - Supports a calculator tool with `calc:` prefix
    - Keeps short-term memory of the conversation
    """
    llm = get_llm()
    notes = load_notes()
    history = []  # list of {"role": "user"/"assistant", "content": str}

    print("🤖 SWE645 Study Assistant Agent (Custom Loop + Ollama)")
    print("Type 'exit' to quit.")
    print("Tip: type `calc: 25 * (3 + 7)` for calculator.\n")

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.strip().lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        # --- Tool 1: calculator (manual trigger with 'calc:' prefix) ---
        if user_input.lower().startswith("calc:"):
            expr = user_input.split("calc:", 1)[1].strip()
            result = calculate(expr)
            print(f"Agent (calculator): {expr} = {result}")
            # keep this in history as well
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": f"{expr} = {result}"})
            continue

        # --- Tool 2: notes search (used automatically as context) ---
        notes_snippet = search_notes(notes, user_input)
        extra_context = ""
        if notes_snippet:
            extra_context = (
                "\n\n---\nHere are some relevant course notes you can use:\n"
                + notes_snippet
            )

        # --- Build messages with short-term memory ---
        system_prompt = (
            "You are a helpful SWE645 Study Assistant. "
            "Use the provided course notes when available. "
            "Explain things clearly like to a fellow student."
        )

        messages = [{"role": "system", "content": system_prompt}]

        for msg in history:
            messages.append(msg)

        user_message_content = user_input + extra_context
        messages.append({"role": "user", "content": user_message_content})

        # --- Call the LLM (Ollama) ---
        try:
            response = llm.invoke(messages)
            # ChatOllama returns an AIMessage with .content
            answer = getattr(response, "content", str(response))
        except Exception as e:
            answer = f"Error from LLM: {e}"

        print("Agent:", answer)

        # --- Update memory ---
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    run_cli()
