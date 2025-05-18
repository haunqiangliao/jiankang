import streamlit as st
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="健康倒计时提醒", layout="wide")
st.title("⏳ 健康倒计时提醒助手")

# 初始化会话状态
if "reminders" not in st.session_state:
    st.session_state.reminders = {
        "饮水": {"interval": 60, "next_reminder": None},
        "运动": {"interval": 120, "next_reminder": None},
        "久坐": {"interval": 30, "next_reminder": None},
    }

def set_reminder(type_, interval):
    """设置提醒时间"""
    now = datetime.now()
    next_time = now + timedelta(seconds=interval)
    st.session_state.reminders[type_]["next_reminder"] = next_time
    st.session_state.reminders[type_]["interval"] = interval

def display_countdown(type_):
    """显示倒计时"""
    reminder = st.session_state.reminders[type_]
    if reminder["next_reminder"]:
        now = datetime.now()
        delta = reminder["next_reminder"] - now
        
        if delta.total_seconds() <= 0:
            st.success(f"⚠️ 请{type_.lower()}！")
            # 自动延后下一次提醒
            set_reminder(type_, reminder["interval"])
        else:
            minutes, seconds = divmod(int(delta.total_seconds()), 60)
            st.info(f"距离下次{type_}提醒还有：{minutes}分{seconds}秒")
    else:
        st.info(f"请先设置{type_}提醒间隔")

# 侧边栏设置间隔
st.sidebar.header("提醒间隔设置（秒）")
for type_ in st.session_state.reminders:
    interval = st.sidebar.slider(f"{type_}间隔", 10, 3600, st.session_state.reminders[type_]["interval"], key=f"{type_}_slider")
    if st.sidebar.button(f"设置{type_}提醒", key=f"{type_}_button"):
        set_reminder(type_, interval)

# 主界面显示倒计时
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("饮水提醒")
    display_countdown("饮水")
    if st.button("立即提醒", key="water_now"):
        set_reminder("饮水", 0)  # 立即触发提醒

with col2:
    st.subheader("运动提醒")
    display_countdown("运动")
    if st.button("立即提醒", key="exercise_now"):
        set_reminder("运动", 0)

with col3:
    st.subheader("久坐提醒")
    display_countdown("久坐")
    if st.button("立即提醒", key="sit_now"):
        set_reminder("久坐", 0)

# 自动刷新页面更新倒计时
if st.session_state.reminders:
    time.sleep(1)
    st.rerun()
