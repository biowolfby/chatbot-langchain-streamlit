import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def main():
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    client = OpenAI(api_key=openai_api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "write a haiku about ai"}
        ],
        temperature=0.7
    )

    print(completion.choices[0].message.content)


if __name__ == "__main__":
    main()
