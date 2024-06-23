import boto3
def QandA():
    # AWS Bedrockクライアントの設定
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    bedrock_client = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')
    # AIに送信するメッセージを作成
    message = {
        "role": "user",
        "content": [{"text": f"物体: {selected_object}\n質問: {question}\nこの質問に対して「はい」か「いいえ」で答えてください。"}]
    }
    messages = [message]
    # 推論に使用するパラメータ
    temperature = 0.5
    top_k = 200
    # ベースの推論パラメータ
    inference_config = {"temperature": temperature}
    # 追加の推論パラメータ
    additional_model_fields = {"top_k": top_k}
    # メッセージの送信
    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        inferenceConfig=inference_config,
        additionalModelRequestFields=additional_model_fields
    )
    # 応答の取得
    output_message = response['output']['message']
    completion_text = output_message['content'][0]['text'].lower()
    if selected_object in completion_text or selected_object in question.lower():
        answer = "It's correct."
    elif 'yes' in completion_text or 'はい' in completion_text:
        answer = "はい"
    elif 'no' in completion_text or 'いいえ' in completion_text:
        answer = "いいえ"
    else:
        answer = "わかりません"