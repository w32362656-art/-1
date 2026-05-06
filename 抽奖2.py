#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import streamlit as st
import random
import time

# 设置页面配置
st.set_page_config(page_title="手机抽奖系统", layout="centered")

# 初始化 Session State
if 'step' not in st.session_state:
    st.session_state.step = "input"
if 'pool' not in st.session_state:
    st.session_state.pool = []
if 'winners' not in st.session_state:
    st.session_state.winners = []

# --- 抽奖结果弹窗 ---
@st.dialog("🎉 恭喜中奖人员")
def show_results():
    st.write("以下是本次中奖名单：")
    for name in st.session_state.winners:
        st.success(f"✨ {name}")
    if st.button("关闭并重置"):
        st.session_state.step = "input"
        st.session_state.winners = []
        st.rerun()

# --- 逻辑页面 ---

# 页面 1: 输入名单
if st.session_state.step == "input":
    st.title("手机抽奖系统")
    input_data = st.text_area("请输入名单 (一行一个)", height=300, placeholder="在此处粘贴名单...")
    
    if st.button("加载名单"):
        names = [n.strip() for n in input_data.split('\n') if n.strip()]
        if names:
            st.session_state.pool = names
            st.session_state.step = "lottery"
            st.rerun()
        else:
            st.error("名单不能为空，请输入后再尝试！")

# 页面 2: 抽奖现场
elif st.session_state.step == "lottery":
    st.title("抽奖现场")
    st.write(f"当前池内总人数: **{len(st.session_state.pool)}**")
    
    # 优化后的名单查看方式：使用 \n\n 强制每行显示一个名字
    with st.expander("查看当前参与名单"):
        formatted_names = "\n\n".join([f"• {name}" for name in st.session_state.pool])
        st.markdown(formatted_names)

    num = st.number_input("设置抽取人数", min_value=1, max_value=len(st.session_state.pool), value=1)
    
    if st.button("开始抽取"):
        st.session_state.winners = []
        progress_bar = st.progress(0)
        status_area = st.empty()
        
        # 逐个抽取逻辑
        for i in range(num):
            status_area.warning(f"正在准备抽取第 {i+1} 位...")
            time.sleep(0.5) 
            
            winner = random.choice(st.session_state.pool)
            st.session_state.pool.remove(winner)
            st.session_state.winners.append(winner)           
            # 显示结果，持续 1 秒
            status_area.success(f"🎉 恭喜第 {i+1} 位中奖者: **{winner}**")
            progress_bar.progress((i + 1) / num)
            
            # 这里的 1.0 即为你要求的每人 1 秒的间隔
            time.sleep(1.0) 
        
        # 抽完后弹出窗口
        show_results()

import streamlit as st

# 注入 PWA 的 manifest 链接和主题色
st.markdown("""
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#ff4b4b">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="apple-mobile-web-app-title" content="抽奖助手">
""", unsafe_allow_html=True)

import streamlit as st

# --- 你的主程序代码区 ---
st.title("抽奖活动页面")
# ... 这里是你的抽奖逻辑 ...

