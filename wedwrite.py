import streamlit as st
import project as p
import app as a

def 一ページ目表示():
    st.set_page_config(layout="wide")
    st.title('AI質問応答システム')
    if st.button('始める'):
        st.rerun

def セットアップ():
    st.title('Setting')
    st.write('質問版は何ですか？')
    # テキストボックスを作成
    question = st.text_input('Yes か No で答えられる質問を書いてしてください', '質問を入力してください')
    # 入力内容を表示
    st.write('質問:', question)
    # ボタンを押すと、質問を表示
    # if st.button('質問を送信'):
    #     アンサー待ち()
    return question

def アンサー待ち():
    st.title('Answer')
    st.write('質問版は何ですか？')
    # テキストボックスを作成
    answer = st.text_input('Yes か No で答えられる質問を書いてしてください', '賳問を入力してください')
    # 入力内容を表示
    st.write('質問:', answer)
    # ボタンを押すと、質問を表示
    if st.button('質問を送信'):
        セットアップ()


一ページ目表示()