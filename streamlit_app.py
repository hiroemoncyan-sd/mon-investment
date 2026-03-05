import streamlit as st
import numpy as np
import random
import time

# --- アプリの設定 ---
st.set_page_config(page_title="My Investment App", layout="centered")

# カスタマイズ：通貨単位（好きな文字に変えてね！）
CURRENCY = "SD" 

# --- データの初期化 ---
if 'cash' not in st.session_state:
    st.session_state.cash = 1000000
    st.session_state.companies = ["Hiroe cafe", "beau chat S&D", "monchi Power", "hiroemon Mobile"]
    st.session_state.prices = {name: [500.0] * 30 for name in st.session_state.companies}
    st.session_state.holds = {name: 0 for name in st.session_state.companies}

# --- 株価更新ロジック ---
def update_prices():
    for name in st.session_state.companies:
        curr_p = st.session_state.prices[name][-1]
        vola = 0.08
        change = random.uniform(-vola, vola) - (curr_p - 500) * 0.0001
        new_p = max(1.0, curr_p + change)
        st.session_state.prices[name].append(new_p)
        if len(st.session_state.prices[name]) > 30:
            st.session_state.prices[name].pop(0)

# タイトル
st.title(f"💹 Asset Simulator ({CURRENCY})")

# 資産表示
total_stock_val = sum(st.session_state.prices[name][-1] * st.session_state.holds[name] for name in st.session_state.companies)
total_assets = st.session_state.cash + total_stock_val

col_a, col_b = st.columns(2)
col_a.metric("Total Assets", f"{int(total_assets):,} {CURRENCY}")
col_b.metric("Cash on Hand", f"{int(st.session_state.cash):,} {CURRENCY}")

st.divider()

# 各銘柄の表示
for name in st.session_state.companies:
    price_list = st.session_state.prices[name]
    current_price = price_list[-1]
    
    with st.container():
        c1, c2 = st.columns([3, 1])
        with c1:
            st.subheader(f"{name}: {current_price:.2f}")
            st.line_chart(price_list, height=150)
        with c2:
            st.write(f"Hold: {st.session_state.holds[name]}")
            if st.button(f"Buy 1000", key=f"b_{name}"):
                if st.session_state.cash >= current_price * 1000:
                    st.session_state.cash -= current_price * 1000
                    st.session_state.holds[name] += 1000
                    st.rerun()
            if st.button(f"Sell All", key=f"s_{name}"):
                st.session_state.cash += current_price * st.session_state.holds[name]
                st.session_state.holds[name] = 0
                st.rerun()

# 最後に更新（Web版はリロードで動く）
update_prices()
time.sleep(1)
st.rerun()
