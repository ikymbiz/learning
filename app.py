# streamlit-app/app.py
import streamlit as st
import importlib.util
import sys
import os
from pathlib import Path

# ページ設定
st.set_page_config(
    page_title="DD Learn Apps",
    page_icon="📚",
    layout="wide"
)

def load_app_module(app_path):
    """指定されたパスのmain.pyをモジュールとして読み込む"""
    # 既存のモジュールをクリーンアップ
    module_name = f"app_module_{hash(app_path)}"
    if module_name in sys.modules:
        del sys.modules[module_name]
    
    spec = importlib.util.spec_from_file_location(module_name, app_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def get_available_apps():
    """pageフォルダとappsフォルダ配下のアプリ一覧を取得"""
    base_dir = Path(__file__).parent
    apps = {}
    
    # アプリ名を日本語名に変換
    app_names = {
        "flags": "🏳️ 国旗クイズ",
        "flash-cal": "🧮 フラッシュあんざん", 
        "flash_numbers": "🔢 フラッシュ・ナンバーズ",
        "math-creator": "🧮 けいさんドリル作成ツール"
    }
    
    # pageフォルダとappsフォルダの両方をチェック
    for folder_name in ["page", "apps"]:
        folder_dir = base_dir / folder_name
        if folder_dir.exists():
            for app_dir in folder_dir.iterdir():
                if app_dir.is_dir():
                    main_py = app_dir / "main.py"
                    if main_py.exists():
                        display_name = app_names.get(app_dir.name, app_dir.name)
                        # フォルダ名を区別するために、重複がある場合はフォルダ名を追加
                        if display_name in apps:
                            display_name = f"{display_name} ({folder_name})"
                        apps[display_name] = str(main_py)
    
    return apps

def disable_page_config(func):
    """st.set_page_configの呼び出しを無効化するデコレータ"""
    def wrapper(*args, **kwargs):
        pass  # 何もしない
    return wrapper

def run_app_generic(app_name, folder_name):
    """汎用的なアプリ実行関数"""
    # st.set_page_configを一時的に無効化
    original_set_page_config = st.set_page_config
    st.set_page_config = disable_page_config(st.set_page_config)
    
    try:
        # 現在のディレクトリを一時的に変更
        original_cwd = os.getcwd()
        app_path = f"{folder_name}/{app_name}"
        os.chdir(app_path)
        
        # モジュールのグローバル環境で実行
        with open("main.py", encoding='utf-8') as f:
            code = f.read()
        exec(code, globals())
        
    finally:
        # 元の設定を復元
        os.chdir(original_cwd)
        st.set_page_config = original_set_page_config

def main():
    st.title("📚 DD Learn Apps")
    st.markdown("学習アプリケーション集")
    
    # 利用可能なアプリを取得
    apps = get_available_apps()
    
    if not apps:
        st.error("利用可能なアプリが見つかりません。")
        return
    
    # サイドバーでアプリ選択
    with st.sidebar:
        st.header("🎯 アプリ選択")
        selected_app = st.selectbox(
            "起動するアプリを選択してください:",
            options=list(apps.keys()),
            index=0
        )
        
        if st.button("🚀 アプリを起動", use_container_width=True):
            st.session_state.current_app = selected_app
            st.session_state.app_path = apps[selected_app]
            st.rerun()
    
    # 選択されたアプリを実行
    if "current_app" in st.session_state and "app_path" in st.session_state:
        st.subheader(f"実行中: {st.session_state.current_app}")
        
        # アプリをリセットするボタンを上部に配置
        if st.button("🏠 アプリ選択に戻る", use_container_width=True):
            # セッション状態をクリーンアップ
            keys_to_delete = []
            for key in st.session_state.keys():
                if key not in ['current_app', 'app_path']:
                    keys_to_delete.append(key)
            for key in keys_to_delete:
                del st.session_state[key]
            
            if "current_app" in st.session_state:
                del st.session_state.current_app
            if "app_path" in st.session_state:
                del st.session_state.app_path
            st.rerun()
        
        st.markdown("---")
        
        try:
            # 特定のアプリの実行
            app_path = st.session_state.app_path
            app_dir = Path(app_path).parent
            app_name = app_dir.name
            folder_name = app_dir.parent.name  # page または apps
            
            if app_name == "flags":
                run_app_generic(app_name, folder_name)
            elif app_name == "flash-cal":
                run_app_generic(app_name, folder_name)
            elif app_name == "flash_numbers":
                run_app_generic(app_name, folder_name)
            elif app_name == "math-creator":
                run_app_generic(app_name, folder_name)
            else:
                st.error(f"未対応のアプリです: {app_name}")
                
        except Exception as e:
            st.error(f"アプリの実行中にエラーが発生しました: {str(e)}")
            st.code(str(e))
    else:
        # アプリが選択されていない場合の表示
        st.info("👈 サイドバーからアプリを選択して起動してください。")
        
        # 利用可能なアプリの一覧表示
        st.subheader("📋 利用可能なアプリ")
        
        cols = st.columns(2)
        for i, (app_name, app_path) in enumerate(apps.items()):
            with cols[i % 2]:
                st.markdown(f"**{app_name}**")
                st.caption(f"パス: {app_path}")

# アプリケーション実行
if __name__ == "__main__":
    main()