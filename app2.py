import streamlit as st
from streamlit_bokeh_events import streamlit_bokeh_events
from bokeh.models import CustomJS
from bokeh.models.widgets import Button
from bokeh.plotting import figure
from bokeh.layouts import column

st.set_page_config(page_title="GPS位置取得", layout="centered")
st.title("📍スマホのGPS位置を取得")

# Streamlit Cloud でエラーにならないようダミーの描画要素（Figure）を追加
dummy_plot = figure(width=100, height=100)
dummy_plot.toolbar_location = None
dummy_plot.outline_line_alpha = 0

# GPS取得ボタンの定義（JavaScriptで位置取得）
loc_button = Button(label="現在地を取得")
loc_button.js_on_event("button_click", CustomJS(code="""
    navigator.geolocation.getCurrentPosition((loc) => {
        document.dispatchEvent(new CustomEvent("GET_LOCATION", {
            detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}
        }))
    })
"""))

# レイアウトして表示（描画要素＋ボタン）
st.bokeh_chart(column(dummy_plot, loc_button))

# イベント待機・取得処理
result = streamlit_bokeh_events(
    loc_button,
    events="GET_LOCATION",
    key="get_location",
    refresh_on_update=False,
    debounce_time=0
)

# 結果の表示
if result and "GET_LOCATION" in result:
    lat = result["GET_LOCATION"]["lat"]
    lon = result["GET_LOCATION"]["lon"]

    st.success(f"✅ 位置情報取得に成功：緯度 {lat}, 経度 {lon}")
    st.map(data={"lat": [lat], "lon": [lon]})
    st.write(result["GET_LOCATION"])
else:
    st.info("スマホで「現在地を取得」ボタンを押して、位置情報取得を許可してください。")
