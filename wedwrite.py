import streamlit as st
import boto3
import random
import pandas as pd
from pprint import pprint
model_id = "anthropic.claude-3-haiku-20240307-v1:0"
bedrock_client = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')
st.set_page_config(layout="wide")
# 物体のリスト
objects = []

def 一ページ目表示():
    st.title('AI質問応答システム')
    if st.button('始める'):
        st.session_state.page = 'setup'
        st.session_state.object = random.choice(objects)
def セットアップ():
    st.title('設定')
    st.write('質問は何ですか？')
    selected_object = st.session_state.object
    st.write(f"選ばれた物体: {selected_object}")
    # テキストボックスを作成
    question = st.text_input('Yes か No で答えられる質問を書いてしてください', placeholder='質問を入力してください')
    # 入力内容を表示
    st.write('質問:', question)
    if st.button('質問を送信'):
        # AIに送信するメッセージを作成
        message = {
            "role": "user",
            "content": [{"text": f"物体: {selected_object}\n質問: {question}\nこの質問に対して「はい」か「いいえ」で答えてください。"}]
        }
        messages = [message]
        # Inference parameters to use.
        temperature = 0.5
        top_k = 200
        # Base inference parameters to use.
        inference_config = {"temperature": temperature}
        # Additional inference parameters to use.
        additional_model_fields = {"top_k": top_k}
        # メッセージを送信
        response = bedrock_client.converse(
            modelId=model_id,
            messages=messages,
            inferenceConfig=inference_config,
            additionalModelRequestFields=additional_model_fields
        )
        # 応答を取得
        output_message = response['output']['message']
        completion_text = output_message['content'][0]['text'].lower()
        # 応答に選ばれた物体が含まれているかチェックして対応するメッセージを表示
        if selected_object in completion_text or selected_object in question.lower():
            st.write('回答:', "It's correct.")
        elif 'yes' in completion_text or 'はい' in completion_text:
            st.write('回答:', "はい")
        elif 'no' in completion_text or 'いいえ' in completion_text:
            st.write('回答:', "いいえ")
        else:
            st.write('回答:', "わかりません")


