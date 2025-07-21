import streamlit as st
from gui import (
    init_session_state,
    setup_page,
    setup_sidebar,
    show_sequence_phase,
    show_input_phase
)
from logic import generate_sequence

def main():
    # 初期化
    init_session_state()
    setup_page()
    setup_sidebar()

    # タイトルとスタート
    st.title("🔢 フラッシュ・ナンバーズ")
    if st.button("▶ スタート", use_container_width=True):
        st.session_state.sequence = generate_sequence(st.session_state.sequence_length)
        st.session_state.started = True
        st.session_state.current_index = 0
        st.session_state.showing_sequence = True
        st.session_state.user_inputs = []
        st.session_state.current_input_index = 0
        st.session_state.showing_result = False
        st.rerun()

    # 各フェーズの表示
    show_sequence_phase()
    show_input_phase()

if __name__ == "__main__":
    main()
