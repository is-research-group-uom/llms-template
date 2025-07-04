import boto3
import json
from credentials import get_bedrock_client

def pixtral(pdf_text):
    bedrock = get_bedrock_client()

    prompt = "Describe the purpose of a 'hello world' program in one line."

    request_body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt,
                        "type": "text"
                    }
                ]
            }
        ],
        "max_tokens": 10
    }

    response = bedrock.invoke_model(
        modelId='arn:aws:bedrock:us-east-1:043309345392:inference-profile/us.mistral.pixtral-large-2502-v1:0',
        body=json.dumps(request_body)
    )

    return json.dumps(json.loads(response.get('body').read()))