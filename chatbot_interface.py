import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_chroma import Chroma


class ChatbotCore:
    def __init__(
            self,
            mistral_api_key=None,
            system_prompt="You are a helpful assistant. Answer all questions to the best of your ability.",
            model="mistral-small-latest",
            temperature=0.7,
        ):
        if mistral_api_key is None:
            load_dotenv()
            mistral_api_key = os.getenv("MISTRAL_API_KEY")
        self.api_key = mistral_api_key
        
        self.embeddings = MistralAIEmbeddings(model="mistral-embed", api_key=self.api_key)
        
        self.vector_store = Chroma(
            embedding_function=self.embeddings,
            persist_directory="chroma_db",
            )
        
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5},
            )

        # Initialize the prompt
        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(system_prompt),
                MessagesPlaceholder(variable_name="conversation", optional=True),
                ("human", "Answer this question using the provided context. Question: {question}. Context: {context}")
            ]
        )

        # Configure the Mistral model
        self.llm = ChatMistralAI(
            api_key=self.api_key, 
            model=model, 
            temperature=temperature
        )

        self.chain = self.prompt | self.llm

        # Initialize conversation history
        self.chat_history = ChatMessageHistory()

    def send_message(self, message):
        """
        Send a message to the chatbot and receive the response.

        Args:
            message (str): The message to send to the chatbot.

        Returns:
            str: The chatbot's response.
        """
        self.chat_history.add_user_message(message)
        history_text = "\n".join(msg.text() for msg in self.chat_history.messages if msg.type == "human")
        print(f"History text: {history_text}")
        # response = self.chain.invoke({"conversation": self.chat_history.messages, "question": message})
        context = self.retriever.invoke(message)
        print(f"Context: {context}")
        response = self.chain.invoke({
            "conversation": self.chat_history.messages,
            "question": message,
            "context": context
        })
        
        self.chat_history.add_ai_message(response.content)
        return response.content
        

    def get_history(self):
        """
        Access the conversation history.

        Returns:
            list: A list of conversation messages.
        """
        return self.chat_history.messages


st.title("💬 Chatbot 27-Mar-2025")
st.caption("🚀 A Streamlit chatbot powered by Mistral")
st.sidebar.success("Select a demo above.")


if __name__ == "__main__":
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = ChatbotCore()

    for msg in st.session_state.chatbot.chat_history.messages:
        st.chat_message("user" if msg.type == "human" else "assistant").write(msg.content)

    if prompt := st.chat_input():
        st.chat_message("user").write(prompt)
        with st.chat_message("assistant"):
            response = st.session_state.chatbot.send_message(prompt)
            st.write(response)