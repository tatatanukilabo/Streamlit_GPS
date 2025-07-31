from bokeh.models import CustomJS
from bokeh.models.widgets import Button
from bokeh.plotting import figure
from bokeh.layouts import column
import streamlit as st
from streamlit_bokeh_events import streamlit_bokeh_events

st.title("スマホのGPS位置を取得")

# ① loc_button を先に定義
loc_button = Button(label="現在地を取得")
loc_button.js_on_event("button_click", CustomJS(code="""
    navigator.geolocation.getCurrentPosition((loc) => {
        document.dispatchEvent(new CustomEvent("GET_LOCATION", {
            detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}
        }))
    })
"""))

# ② ダミーのグラフを追加して描画可能にする
dummy_fig = figure(width=0, height=0)
layout = column(dummy_fig, loc_button)

# ③ Streamlit に表示
st.bokeh_chart(layout)

# ④ イベント取得
result = streamlit_bokeh_events(
    loc_button,
    events="GET_LOCATION",
    key="get_location",
    refresh_on_update=False,
    debounce_time=0
)

if result and "GET_LOCATION" in result:
    lat = result["GET_LOCATION"]["lat"]
    lon = result["GET_LOCATION"]["lon"]
    st.success(f"位置情報を取得しました：緯度 {lat}, 経度 {lon}")
    st.map(data={"lat": [lat], "lon": [lon]})
