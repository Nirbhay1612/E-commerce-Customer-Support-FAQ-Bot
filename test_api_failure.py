from http import client
from unittest.mock import Mock
from groq import Groq

def test_api_failure():
    # Fake the Groq client
    client=Mock(spec=Groq)

    #stimulate API failure
    client.chat.completions.create.side_effect = Exception (
        "Stimulated API Failure"
    )
    try:
        client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "user",
                  "content": "Where is my order"}
                  ],
        )
    except Exception as e:
        print("API failure Handled Successfully!")
        print("Error:",e)

        if __name__=="__main__":
            test_api_failure()
    