#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import random
import time

st.set_page_config(page_title="抽奖系统")
st.title("手机抽奖系统")

# 初始化奖池
if 'pool' not in st.session_state:
    st.session_state.pool = []

# 1. 调整输入框高度 (height 参数)
input_data = st.text_area("请输入名单 (一行一个)", height=200)

if st.button("加载名单"):
    st.session_state.pool = [n.strip() for n in input_data.split('\n') if n.strip()]
    st.success(f"名单已更新，当前共 {len(st.session_state.pool)} 人")

st.write(f"当前池内人数: {len(st.session_state.pool)}")
num = st.number_input("抽取人数", min_value=1, value=1)

# 2. 定义弹窗内容
@st.dialog("🎉 抽奖结果")
def show_winners(winners):
    st.write("恭喜以下中奖者：")
    for i, winner in enumerate(winners, 1):
        st.success(f"{i}. {winner}")
    if st.button("关闭"):
        st.rerun()

# 3. 开始抽奖逻辑
if st.button("开始抽奖"):
    if len(st.session_state.pool) < num:
        st.error("池内人数不足，无法抽取！")
    else:
        # 使用进度条代替气球动画，更简洁
        progress_bar = st.progress(0)
        status_text = st.empty()

        results = []
        for i in range(num):
            status_text.text(f"正在抽取第 {i+1} 位...")
            time.sleep(0.5) # 模拟抽奖动效
            winner = random.choice(st.session_state.pool)
            st.session_state.pool.remove(winner)
            results.append(winner)
            progress_bar.progress((i + 1) / num)

        status_text.text("抽奖完成！")
        # 弹出结果窗口
        show_winners(results)

