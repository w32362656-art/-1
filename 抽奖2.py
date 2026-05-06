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
        # 去除空行并清理空格
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
