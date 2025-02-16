import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_mistralai import ChatMistralAI


class ChatbotCore:
    def __init__(
            self,
            mistral_api_key=None,
            system_prompt="You are a helpful assistant. Answer all questions to the best of your ability.",
            model="pixtral-12b-2409",
            temperature=0.7,
    ):
        if mistral_api_key is None:
            load_dotenv()
            mistral_api_key = os.getenv("MISTRAL_API_KEY")
        self.api_key = mistral_api_key

        # Initialize the prompt
        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(system_prompt),
                MessagesPlaceholder(variable_name="messages"),
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
