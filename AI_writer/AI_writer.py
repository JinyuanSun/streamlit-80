import streamlit as st
from openai import OpenAI
st.set_page_config(layout="wide")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Set OpenAI API key from Streamlit secrets
openai_aip_key = st.sidebar.text_input("OpenAI API Key", type="password")
if openai_aip_key == st.secrets["LABPASS"]:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    client = OpenAI(api_key=openai_aip_key)
if "text" not in st.session_state:
    st.session_state["text"] = ""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant to help user write better scientific papers. Answer user questions using markdown."}]

with st.sidebar:
    st.title("Chat Area")
    messages_container = st.container(height=500)



# Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with messages_container.chat_message(message["role"]):
            if message["role"] == "assistant":
                messages_container.markdown(message["content"])
            if message["role"] == "user":
                messages_container.markdown(message["content"].split("\ncurrent text:\n")[0])

# Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        prompt += f"\ncurrent text:\n {st.session_state['text']}"
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with messages_container.chat_message("user"):
            messages_container.markdown(prompt.split("\ncurrent text:\n")[0])
        # Display assistant response in chat message container
        with messages_container.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = messages_container.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

col_left, _, col_right = st.columns([4.9,0.2,4.9])


# while True:


with col_left:
    st.title("Writing area")
    st.session_state["text"] = st.text_area(label="Writing area 1", 
                                            height=600, 
                                            # value=st.session_state["text"],
                                            label_visibility="collapsed")

if st.sidebar.button("Update Markdown"):
    st.session_state["text"] = st.session_state.messages[-1]["content"]

with col_right:
    st.title("Rendered markdown")
    with st.container(border=1, height=600):
        st.markdown(st.session_state["text"])

