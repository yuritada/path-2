import streamlit as st
# SessionStateを使って、ボタンの状態を保持する
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

# ボタンを表示
if st.button('表示する'):
    st.session_state.button_clicked = True

# 表示されたテキストをリセットするボタン
if st.button('リセット'):
    st.session_state.button_clicked = False
    a = 1
    print(f"(a: {a})")

    st.rerun()

# ボタンがクリックされた状態ならテキストを表示する
if st.session_state.button_clicked:
    st.write("このテキストは表示/非表示を切り替えることができます。")
