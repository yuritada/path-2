# import boto3

# # s3とは、AWSのオブジェクトストレージサービス
# # boto3は、AWSのサービスを利用するためのPythonライブラリ
# # boto3.resourceで、AWSのリソースを扱うためのオブジェクトを生成
# # オブジェクトとは、データとそれに関連する操作をまとめたもの
# s3 = boto3.resource('s3')

import boto3
import wedwrite as wr
from pprint import pprint

def QandA ():
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    system_prompt = "あなたは多くのデータにアクセス可能な経済学者です。"
    prompt = wr.セットアップ()
    bedrock_client = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')
    # Message to send.
    message = {
        "role": "user",
        "content": [{"text": prompt}]
    }
    messages = [message]
    system_prompts = [{"text" : system_prompt}]
    # Inference parameters to use.
    temperature = 0.5
    top_k = 200
    # Base inference parameters to use.
    inference_config = {"temperature": temperature}
    # Additional inference parameters to use.
    additional_model_fields = {"top_k": top_k}
    # Send the message.
    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        inferenceConfig=inference_config,
        additionalModelRequestFields=additional_model_fields
    )
    # pprint(response)
    # print("=" * 30)
    output_message = response['output']['message']
    # print(f"Role: {output_message['role']}")
    # print(f"Text: {output_message['content'][0]['text']}")
    # token_usage = response['usage']
    # print(f"Input tokens:  {token_usage['inputTokens']}")
    # print(f"Output tokens:  {token_usage['outputTokens']}")
    # print(f"Total tokens:  {token_usage['totalTokens']}")
    # print(f"Stop reason: {response['stopReason']}")

    return (f"(TEXT: {output_message['content'][0]['text']})")