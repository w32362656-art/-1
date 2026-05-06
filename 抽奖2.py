#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import random
import time

st.set_page_config(page_title="手机抽奖系统")

# 初始化状态
if 'step' not in st.session_state:
    st.session_state.step = "input"  # 初始页面：输入
if 'pool' not in st.session_state:
    st.session_state.pool = []
if 'winners' not in st.session_state:
    st.session_state.winners = []

# --- 弹窗逻辑 ---
@st.dialog("🏆 本轮中奖名单")
def show_results():
    for name in st.session_state.winners:
        st.success(f"🎉 {name}")
    if st.button("返回首页"):
        st.session_state.step = "input"
        st.session_state.winners = []
        st.rerun()

# --- 页面 1: 输入名单 ---
if st.session_state.step == "input":
    st.title("手机抽奖系统 - 第一步")
    input_data = st.text_area("请输入名单 (一行一个)", height=300)
    if st.button("加载名单"):
        st.session_state.pool = [n.strip() for n in input_data.split('\n') if n.strip()]
        if st.session_state.pool:
            st.session_state.step = "lottery"
            st.rerun()
        else:
            st.error("名单不能为空！")

# --- 页面 2: 抽奖过程 ---
elif st.session_state.step == "lottery":
    st.title("手机抽奖系统 - 抽奖现场")
    st.write(f"当前池内总人数: **{len(st.session_state.pool)}**")
    
    with st.expander("查看当前名单"):
        st.write(st.session_state.pool)

    num = st.number_input("设置抽取人数", min_value=1, max_value=len(st.session_state.pool), value=1)
    
    if st.button("开始抽取"):
        st.session_state.winners = [] # 清空上一次结果
        progress_bar = st.progress(0)
        status_area = st.empty() # 用于展示当前中奖者的区域
        
        # 逐个抽取逻辑
        for i in range(num):
            winner = random.choice(st.session_state.pool)
            st.session_state.pool.remove(winner)
            st.session_state.winners.append(winner)
            
            # 视觉反馈：显示当前中奖者
            status_area.info(f"正在抽取... 恭喜第 {i+1} 位中奖者: **{winner}**")
            progress_bar.progress((i + 1) / num)
            time.sleep(1) # 这里控制名单出来的间隔时间
        
        # 抽完后弹出窗口
        show_results()
