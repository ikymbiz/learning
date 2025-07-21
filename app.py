# streamlit-app/app.py
import dotenv
import streamlit as st
import os

# ページ設定
st.set_page_config(
    page_title="DD Learn Apps",
    page_icon="📚",
    layout="wide"
)

def main():
    base_dir = os.path.dirname(__file__) or '.'
    app_dir = os.path.join(base_dir, 'apps')
    home = st.Page(page=home_page, title="home", url_path="home", default=True)

    # appフォルダ直下のフォルダ名のみを取得
    page_list = [name for name in os.listdir(app_dir)
                 if os.path.isdir(os.path.join(app_dir, name))]
    navigation_list = [home]

    for i, page in enumerate(page_list):
        app_path = os.path.join(base_dir, "apps", page, "main.py")
        if os.path.exists(app_path):
            navigation_list.append(st.Page(page=app_path, title=page, url_path=page, default=False))
        else:
            st.error(f"ファイルが見つかりません: {app_path}")

    pg = st.navigation(navigation_list, position="hidden")
    pg.run()

def home_page():
    dotenv.load_dotenv()
    url_path = os.getenv("URL_PATH")

    # Automatic redirect after showing title
    st.markdown(f'<meta http-equiv="refresh" content="2; url={url_path}">', unsafe_allow_html=True)
    st.markdown(f"Redirecting to {url_path} in 2 seconds...")

if __name__ == '__main__':
    main()