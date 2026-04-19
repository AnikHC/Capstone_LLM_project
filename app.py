import streamlit as st


from graph import graph   # or adjust if needed

st.set_page_config(page_title="AI Course Assistant", layout="wide")

st.title("AI Course Assistant")
st.write("Ask questions based on your documents")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Enter your question:")

if st.button("Ask") and query:
    state = {
        "question": query,
        "history": st.session_state.history
    }

    result = graph.invoke(state)

    answer = result["answer"]
    evaluation = result.get("evaluation", "")

    st.session_state.history = result["history"]

    st.subheader("Answer")
    st.write(answer)

    st.subheader("Evaluation")
    st.write(evaluation)

if st.session_state.history:
    st.subheader("Conversation History")

    for item in st.session_state.history:
        st.write(item)