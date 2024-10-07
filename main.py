import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage("You are a helpful assistant. Answer all questions to the best of your ability."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4o-mini", temperature=0.7)

chain = prompt | llm

chat_history = ChatMessageHistory()


def main():
    while True:
        user_input = input("You: ")
        chat_history.add_user_message(user_input)

        response = chain.invoke({"messages": chat_history.messages})
        print("Assistant:", response.content)

        chat_history.add_ai_message(response.content)


if __name__ == "__main__":
    main()
