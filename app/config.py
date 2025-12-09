from langchain_community.chat_models import ChatOllama
# or: from langchain_ollama import ChatOllama  (if you installed langchain-ollama)


def get_llm():
    """
    Returns the main LLM used by the agent, using a local Ollama model.
    """
    return ChatOllama(
        model="llama3.1",   # make sure you ran: `ollama pull llama3.1`
        temperature=0.2,
    )
