import streamlit as st
import time
from logic import generate_sequence, normalize_input, check_sequence

def init_session_state():
    """セッション状態を初期化する"""
    for key, val in {
        "sequence": [],
        "started": False,
        "start_time": 0.0,
        "correct_count": 0,
        "total_count": 0,
        "current_index": 0,
        "showing_sequence": False,
        "user_inputs": [],
        "current_input_index": 0,
        "showing_result": False,
        "result_correct": False,
        "result_time": 0.0,
    }.items():
        if key not in st.session_state:
            st.session_state[key] = val

def setup_page():
    """ページの基本設定を行う"""
    st.set_page_config(page_title="フラッシュ・ナンバーズ", layout="centered", initial_sidebar_state="collapsed")
    
    # スタイル設定
    st.markdown("""
    <style>
    .number-display {
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
        color: black;
        padding: 60px 40px;
        margin: 30px 0;
        border-radius: 20px;
        text-align: center;
        font-size: 96px;
        font-weight: bold;
        font-family: 'Arial', sans-serif;
        min-height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .stButton > button {
        height: 60px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        margin: 2px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def setup_sidebar():
    """サイドバーの設定を行う"""
    with st.sidebar:
        st.header("⚙️ 設定")
        st.session_state.sequence_length = st.number_input("表示する数字の数", min_value=2, max_value=10, value=3)
        st.session_state.display_speed = st.slider("表示速度（秒）", 0.01, 2.0, 0.8, 0.01)
        
        # 正解率の表示
        if st.session_state.total_count > 0:
            acc = round(100 * st.session_state.correct_count / st.session_state.total_count, 1)
            st.metric(
                "正解率",
                f"{acc}%",
                f"{st.session_state.correct_count}/{st.session_state.total_count}"
            )

def show_sequence_phase():
    """数字表示フェーズ"""
    if st.session_state.started and st.session_state.showing_sequence:
        if st.session_state.current_index < len(st.session_state.sequence):
            display = str(st.session_state.sequence[st.session_state.current_index])
            st.markdown(f"<div class='number-display'>{display}</div>", unsafe_allow_html=True)
            time.sleep(st.session_state.display_speed)
            st.session_state.current_index += 1
            st.rerun()
        else:
            st.session_state.showing_sequence = False
            st.session_state.started = False
            st.session_state.start_time = time.time()
            st.rerun()

def show_input_phase():
    """入力フェーズ"""
    # 問題が存在し、表示フェーズが終わっている場合
    if st.session_state.sequence and not st.session_state.showing_sequence:
        st.markdown("<div class='number-display'>こたえは？</div>", unsafe_allow_html=True)
        
        # 入力表示
        input_display = "　".join(str(st.session_state.user_inputs[i]) if i < len(st.session_state.user_inputs) else "□" 
                                for i in range(len(st.session_state.sequence)))

        st.subheader(f"🔢 にゅうりょく: {input_display}")

        # 数字パッド
        for row in range(3):
            cols = st.columns(3)
            for col in range(3):
                with cols[col]:
                    num = row * 3 + col + 1
                    if st.button(str(num), key=f"btn{num}", use_container_width=True):
                        handle_input(num)
                        st.rerun()

        # 0と操作ボタン
        col0, colback, colsubmit = st.columns(3)
        with col0:
            if st.button("0", key="btn0", use_container_width=True):
                handle_input(0)
                st.rerun()
        with colback:
            if st.button("⌫", key="btnback", use_container_width=True):
                if st.session_state.user_inputs:
                    st.session_state.user_inputs.pop()
                    st.session_state.current_input_index -= 1
                st.rerun()
        with colsubmit:
            if st.button("こたえあわせ", key="btnsubmit", use_container_width=True):
                check_answer()
                st.rerun()

        # 結果表示（電卓パッドの下）
        if st.session_state.showing_result:
            if st.session_state.result_correct:
                st.success(f"✅ せいかい！（{st.session_state.result_time} びょう）")
            else:
                st.error(f"❌ まちがい！せいかい：{' '.join(map(str, st.session_state.sequence))}（{st.session_state.result_time} びょう）")
            
            # 正解率の表示
            if st.session_state.total_count > 0:
                acc = round(100 * st.session_state.correct_count / st.session_state.total_count, 1)
                st.info(f"📊 正解率: {acc}% ({st.session_state.correct_count}/{st.session_state.total_count})")

def handle_input(num):
    """入力処理"""
    if st.session_state.current_input_index < len(st.session_state.sequence):
        st.session_state.user_inputs.append(num)
        st.session_state.current_input_index += 1
        
        # 全ての入力が完了したら答え合わせ
        if st.session_state.current_input_index >= len(st.session_state.sequence):
            check_answer()

def check_answer():
    """答え合わせ"""
    is_correct = check_sequence(st.session_state.user_inputs, st.session_state.sequence)
    elapsed = round(time.time() - st.session_state.start_time, 2)
    st.session_state.total_count += 1
    
    if is_correct:
        st.session_state.correct_count += 1
    
    # 結果を保存
    st.session_state.showing_result = True
    st.session_state.result_correct = is_correct
    st.session_state.result_time = elapsed
    
    # 結果表示のために画面を更新
    st.rerun() 