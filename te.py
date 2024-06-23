import streamlit as st
import boto3
import random
import json
import base64
from datetime import datetime

# AWS Bedrockクライアントの設定
runtime_client = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')

# プロンプトとスタイルの設定
prompt_data = "cat"
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
    "height": 512,
    "width": 512,
})

# モデル推論の実行
response = runtime_client.invoke_model(body=body, modelId=modelId)

# レスポンスから画像データを抽出
response_body = json.loads(response.get("body").read())
base64_data = response_body.get("artifacts")[0]['base64']
binary_data = base64.b64decode(base64_data)

# 画像を保存
dt_str = str(datetime.now())
file_path = f"{dt_str}.png"
with open(file_path, "wb") as f:
    f.write(binary_data)

# Streamlitアプリケーション
st.title('生成された画像')
st.image(file_path, caption='Generated Image', use_column_width=True)
