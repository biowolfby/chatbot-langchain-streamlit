import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI


class ChatbotCore:
    def __init__(
            self,
            openai_api_key=None,
            system_prompt="You are a helpful assistant. Answer all questions to the best of your ability.",
            model="gpt-4o-mini",
            temperature=0.7,
    ):
        if openai_api_key is None:
            load_dotenv()
            openai_api_key = os.getenv("OPENAI_API_KEY")
        self.api_key = openai_api_key

        # Initialiser le prompt
        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(system_prompt),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        # Configurer le modèle de langage
        self.llm = ChatOpenAI(
            api_key=self.api_key, model=model, temperature=temperature
        )

        self.chain = self.prompt | self.llm

        # Initialiser l'historique de conversation
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
        response = self.chain.invoke({"messages": self.chat_history.messages})
        self.chat_history.add_ai_message(response.content)
        return response.content

    def get_history(self):
        """
        Access the conversation history.

        Returns:
            list: A list of conversation messages.
        """
        return self.chat_history.messages
