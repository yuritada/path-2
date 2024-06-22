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

# CSVファイルを読み込み、リストに変換する関数
def load_objects_from_csv(file_path):
    df = pd.read_csv(file_path, header=None)
    return df[0].tolist()

# 例として、"objects.csv"という名前のCSVファイルからデータを読み込みます
csv_file_path = "/Users/masahidesekiguchi/Documents/GitHub/path-2/choice.csv"  # ここに実際のファイルパスを指定してください
objects = load_objects_from_csv(csv_file_path)

def 一ページ目表示():
    st.title('AI質問応答システム')
    if st.button('始める'):
        st.session_state.page = 'setup'
        st.session_state.object = random.choice(objects)

def セットアップ():
    st.title('設定')
    st.write('質問は何ですか？')
    selected_object = st.session_state.object
    # テキストボックスを作成
    question = st.text_input('Yes か No で答えられる質問を書いてしてください', placeholder='質問を入力してください')
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
            answer = "It's correct."
        elif 'yes' in completion_text or 'はい' in completion_text:
            answer = "はい"
        elif 'no' in completion_text or 'いいえ' in completion_text:
            answer = "いいえ"
        else:
            answer = "わかりません"
        st.session_state.question_list.append(question)
        st.session_state.answer_list.append(answer)

    # 質問と回答を表示（新しいものが上部に表示されるように逆順で表示）
    for i in reversed(range(len(st.session_state.question_list))):
        st.write(f"質問{i+1}: {st.session_state.question_list[i]}")
        st.write(f"回答{i+1}: {st.session_state.answer_list[i]}")

# 初期ページを設定
if 'page' not in st.session_state:
    st.session_state.page = 'home'
    st.session_state.question_list = []
    st.session_state.answer_list = []

# ページの切り替え
if st.session_state.page == 'home':
    一ページ目表示()
elif st.session_state.page == 'setup':
    セットアップ()
