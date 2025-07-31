from streamlit_geolocation import streamlit_geolocation
import streamlit as st

location = streamlit_geolocation()

if location and location['latitude'] is not None and location['longitude'] is not None:
    st.write(f"緯度：{location['latitude']}")
    st.write(f"軽度：{location['longitude']}")
else:
    st.warning("位置情報が取得できませんでした。スマホの設定やブラウザの許可を確認してください。")
