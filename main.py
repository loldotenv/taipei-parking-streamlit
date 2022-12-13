from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st
import requests


@st.cache(ttl=600, show_spinner=False)
def get_info(id_filters: Optional[list[str]] = None):
    payload = {
        "$token": "iXE5sPCXMfpjgcucMrWcQd6FbJlAJqQsrAAqCHGSCg8",
        "$format": "json",
    }
    res = requests.get(
        "https://www.ttcx.dot.gov.taipei/cpt/api/OutsideTheRoadsideBasicMaster", params=payload
    )

    if id_filters:
        return list(filter(lambda x: x["id"] in id_filters, res.json()))
    return res.json()


@st.cache(ttl=60, show_spinner=False)
def get_live_data(id_filters: Optional[list[str]] = None):
    url = "https://www.ttcx.dot.gov.taipei/cpt/api/ParkingRemainingData"
    payload = {
        "$token": "iXE5sPCXMfpjgcucMrWcQd6FbJlAJqQsrAAqCHGSCg8",
        "$format": "json",
    }
    res = requests.get(url, params=payload)

    if id_filters:
        return list(filter(lambda x: x["id"] in id_filters, res.json()))
    return res.json()


info = get_info()
tab1, tab2 = st.tabs(["即時車位", "停車場資訊"])
with tab1:
    minutes = None
    seconds = None

    selected = st.multiselect(
        "搜尋", options=[p["name"] for p in info], default=["建國北路高架橋下F區", "建國北路高架橋下H區", "建國北路高架橋下G區"]
    )
    ids = [p["id"] for p in info if p["name"] in selected]
    data = get_live_data(ids)

    for d in data:
        for lot in info:
            if lot["id"] == d["id"]:
                break
        else:
            break
        update_time = datetime.strptime(d["srcUpdateTime"], "%Y-%m-%d %H:%M:%S").astimezone()
        now = datetime.now(ZoneInfo("Asia/Taipei"))
        time_from_update = now - update_time

        minutes = time_from_update.seconds // 60
        seconds = time_from_update.seconds % 60

        col1, col2 = st.columns(2)
        with col1:
            st.subheader(lot["name"])
            st.caption(lot["address"])
        with col2:
            st.metric(f"剩餘車位", f'{max(0, d["availableCar"])} / {lot["totalCar"]}')
        st.markdown("""---""")

    if minutes and seconds:
        st.caption(f"{minutes}分{seconds}秒前更新")

# with tab2:

#     st.text(selected)
#     for lot in info:
#         if lot["name"] == selected:
#             st.text(lot)
