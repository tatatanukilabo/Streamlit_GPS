import streamlit as st
from bokeh.models import CustomJS
from bokeh.models.widgets import Button
from streamlit_bokeh_events import streamlit_bokeh_events

st.title("スマホのGPS位置を取得")

loc_button = Button(label="現在地を取得")
loc_button.js_on_event("button_click", CustomJS(code="""
    navigator.geolocation.getCurrentPosition((loc) => {
        document.dispatchEvent(new CustomEvent("GET_LOCATION", {
            detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}
        }))
    })
"""))

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
    st.write(result["GET_LOCATION"])
