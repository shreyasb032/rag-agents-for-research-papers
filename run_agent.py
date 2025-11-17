from src.VectorStore import VectorStore
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
import streamlit as st

# ------------- Set up the Agent -------------------------------------
if not 'rag_agent' in st.session_state:
    vector_store = VectorStore(document_dir="files")
    vector_store.prepare_documents()
    vs = vector_store.get_vector_store()
    model = init_chat_model("google_genai:gemini-2.5-pro")

    @tool(response_format="content_and_artifact")
    def retrieve_context(query: str):
        """Retrieve information to help answer a query."""
        retrieved_docs = vs.similarity_search(query, k=2)
        serialized = "\n\n".join(
            (f"Source: {doc.metadata}\nContent: {doc.page_content}")
            for doc in retrieved_docs
        )
        return serialized, retrieved_docs

    # Set up the agent with the retrieval tool
    tools = [retrieve_context]

    # Add system prompt to guide the agent's behavior
    prompt = (
        "You are an AI agent designed to assist users by answering their questions. "
        "You have access to a tool that retrieves context from a few"
        " research papers about human-robot interaction. "
        "Use the tool to help answer user queries."
    )

    agent = create_agent(model, tools, system_prompt=prompt)
    st.session_state['rag_agent'] = agent
    print("Agent initialized and ready.")

# # Change the query to test different interactions
# print("Asking the agent a question...")
# query = (
# "Tell me more about the three interaction strategies used in the paper titled " \
# "```Evaluating the impact of personalized value alignment in "
# "human-robot interaction: Insights into trust and team performance outcomes``` "
# )

# # Stream the agent's response
# for event in agent.stream(
#     {"messages": [{"role": "user", "content": query}]},
#     stream_mode="values",
# ):
#     event["messages"][-1].pretty_print()

# ----------------------------------------------------------------------
# -------------- Build the Chat Interface ------------------------------

st.set_page_config(page_title="AI Chat Demo", layout="centered")

st.title("🤖 AI Chat Demo")
st.markdown("Chat with your AI agent below. Uses Google Gemini 2.5 Pro backend!")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for msg in st.session_state.messages:
    if msg["sender"] == "user":
        st.markdown(f'<div style="text-align: right; color: #358AB0;">**You:** {msg["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: left; color: #52B804;">**AI:** {msg["text"]}</div>', unsafe_allow_html=True)

user_input = st.chat_input("Type your message...")

if user_input and user_input.strip() != "":
    # Add user message
    st.session_state.messages.append({"sender": "user", "text": user_input.strip()})
    # Trigger a placeholder AI response
    # st.session_state.messages.append({"sender": "ai", "text": "AI agent response..."})

    # Get the agent's response
    agent = st.session_state['rag_agent']
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": user_input.strip()}]},
        stream_mode="updates",
    ):
        response_text = ""
        for step, data in chunk.items():
            response_dict = data['messages'][-1].content_blocks[-1]
            if step == "model" and 'text' in response_dict:
                response_text += response_dict['text']
        if response_text != '':
            st.session_state.messages.append({"sender": "ai", "text": response_text})


