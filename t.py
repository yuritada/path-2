import streamlit as st
import boto3
import random
import pandas as pd
import json
import base64
from datetime import datetime

# AWS Bedrockクライアントの設定
model_id = "anthropic.claude-3-haiku-20240307-v1:0"
bedrock_client = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')

st.set_page_config(layout="wide")

# 物体のリストをCSVファイルから読み込む関数
def load_objects_from_csv(file_path):
    df = pd.read_csv(file_path, header=None)
    return df[0].tolist()

# CSVファイルから物体のリストを読み込む（ここで実際のファイルパスを指定してください）
csv_file_path = "choice.csv"
objects = load_objects_from_csv(csv_file_path)

# ゲームのリセット関数
def reset_game():
    st.session_state.object = random.choice(objects)
    selected_elements = random.sample(objects, 2)
    selected_elements.append(st.session_state.object)
    st.session_state.question_list = []
    st.session_state.answer_list = []

# 初めのページの表示
def show_start_page():
    st.title('生成AIアキネーター')
    if st.button('始める'):
        reset_game()
        st.session_state.page = 'setup'

# ゲームのセットアップページの表示
def show_setup_page():
    st.title('生成AIアキネータースタート！！')
    selected_object = st.session_state.object
    
    st.write('')  # スペースを作成してボタンと質問フォームの間を区切る

    if st.button('生成された画像を見る'):
        if 'image_file_path' not in st.session_state:
            create_and_save_image()
        st.image(st.session_state.image_file_path, caption='Generated Image', width=512)
    
    with st.form(key='question_form', clear_on_submit=True):
        question = st.text_input('Yes か No で答えられる質問を書いてください', placeholder='質問を入力してください')
        if not question and len(st.session_state.question_list) >= 1:
            st.warning('質問を入力してください')  # 質問が空の場合のメッセージ
        submit_button = st.form_submit_button(label='質問を送信')
        st.write('')
        st.write('')
        col1, col2 = st.columns([4, 1])  # 比率を調整して右端に表示
        with col2:
            view_answer_button = st.form_submit_button(label='答えを見る', use_container_width=True)
            if view_answer_button:
                st.write(f"選ばれた物体: {selected_object}")
    
    if submit_button:
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
        # 応答に選ばれた物体が含まれているかチェックし、対応するメッセージを表示
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
    
    # "正解です！"と表示された場合、「タイトルに戻る」ボタンと「もう一度」ボタンを表示
    if len(st.session_state.answer_list) > 0 and st.session_state.answer_list[-1] == "It's correct.":
        st.write("正解です！")
        col1, col2, col3 = st.columns([4, 1, 1])
        with col2:
            if st.button('タイトルに戻る'):
                st.session_state.page = 'home'
                reset_game()
        with col3:
            if st.button('もう一度'):
                reset_game()
                st.session_state.page = 'setup'
    
    # 質問と回答を逆順で表示する（新しいものが上部に表示されるように）
    for i in reversed(range(len(st.session_state.question_list))):
        st.write(f"質問{i+1}: {st.session_state.question_list[i]}")
        st.write(f"回答{i+1}: {st.session_state.answer_list[i]}")

# 画像を生成して保存する関数
def create_and_save_image():
    global completion_text
    henkan()
    runtime_client = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')
    prompt_data = f"{completion_text}"
    print(prompt_data)
    style_data = "cinematic"  # 他のスタイル: "3d-model", "analog-film", "cinematic", etc.
    # 乱数シードの設定
    seed = random.randint(0, 4294967295)

    # モデルIDとリクエストボディの設定
    modelId = "stability.stable-diffusion-xl-v1"
    body = json.dumps({
        "text_prompts": [
            {
                "text": prompt_data,
                "weight": 1.0
            },
            {
                "text": "artifact",
                "weight": -0.5
            }
        ],
        "samples": 1,
        "cfg_scale": 7,
        "seed": seed,
        "steps": 30,
        "style_preset": style_data,
        "height": 1024,
        "width": 1024,
    })

    # モデル推論の実行
    response = runtime_client.invoke_model(body=body, modelId=modelId)

    # レスポンスから画像データを抽出
    response_body = json.loads(response.get("body").read())
    base64_data = response_body.get("artifacts")[0]['base64']
    binary_data = base64.b64decode(base64_data)

    # 画像を保存
    dt_str = str(datetime.now())#dt_strt
    file_path = f"{dt_str}.png"
    with open(file_path, "wb") as f:
        f.write(binary_data)
    
    # 生成した画像ファイルのパスをセッションに保存
    st.session_state.image_file_path = file_path

def henkan():
    global completion_text
    message = {
            "role": "user",
            "content": [{"text": f"{st.session_state.object}"+"から連想される言葉を英語で3つ返してください。"}]
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

# セッションの初期化
if 'page' not in st.session_state:
    st.session_state.page = 'home'
    st.session_state.question_list = []
    st.session_state.answer_list = []

# ページの表示
if st.session_state.page == 'home':
    show_start_page()
elif st.session_state.page == 'setup':
    show_setup_page()