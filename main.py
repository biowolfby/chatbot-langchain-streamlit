from chatbot_core import ChatbotCore


def main():
    chatbot_core = ChatbotCore()

    while True:
        user_input = input("You: ")
        response = chatbot_core.send_message(user_input)
        print("Assistant:", response)


if __name__ == "__main__":
    main()
