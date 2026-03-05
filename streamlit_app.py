import streamlit as st
import numpy as np
import random
import time
from datetime import datetime, timedelta
from streamlit_local_storage import LocalStorage

# --- アプリの設定 ---
st.set_page_config(page_title="My Investment App", layout="centered")
CURRENCY = "SD" 
local_storage = LocalStorage()

# --- データの初期化 ---
if 'cash' not in st.session_state:
    st.session_state.cash = 1000000
    st.session_state.companies = ["Hiroe cafe", "beau chat S&D", "monchi Power", "hiroemon Mobile"]
    st.session_state.prices = {name: [500.0] * 30 for name in st.session_state.companies}
    st.session_state.holds = {name: 0 for name in st.session_state.companies}
    st.session_state.costs = {name: 0.0 for name in st.session_state.companies}
    st.session_state.date = datetime(2026, 3, 5)
    st.session_state.news = "市場は穏やかです。"

# --- サイドバー：データ管理 ---
st.sidebar.header("💾 データ管理")
if st.sidebar.button("現在の資産をブラウザに保存"):
    save_data = {
        "cash": st.session_state.cash,
        "holds": st.session_state.holds,
        "costs": st.session_state.costs,
        "date": st.session_state.date.strftime("%Y-%m-%d")
    }
    local_storage.set("my_investment_data_final", save_data)
    st.sidebar.success("ブラウザに保存しました！")

if st.sidebar.button("保存したデータから再開"):
    load_data = local_storage.get("my_investment_data_final")
    if load_data:
        st.session_state.cash = load_data["cash"]
        st.session_state.holds = load_data["holds"]
        st.session_state.costs = load_data.get("costs", {name: 0.0 for name in st.session_state.companies})
        st.session_state.date = datetime.strptime(load_data["date"], "%Y-%m-%d")
        st.sidebar.success("データを読み込みました！")
        st.rerun()

# --- 株価更新ロジック ---
def update_prices():
    st.session_state.date += timedelta(days=1)
    impact = 0
    target_company = ""
    if random.random() < 0.1:
        event_type = random.choice(["good", "bad"])
        target_company = random.choice(st.session_state.companies)
        if event_type == "good":
            impact = random.uniform(0.1, 0.3)
            st.session_state.news = f"🔥 【速報】{target_company}の新サービスがヒット！"
        else:
            impact = random.uniform(-0.3, -0.1)
            st.session_state.news = f"😱 【警告】{target_company}で不祥事発覚..."
    else:
        st.session_state.news = "☕ 大きなニュースはありません。"

    for name in st.session_state.companies:
        curr_p = st.session_state.prices[name][-1]
        vola = 0.08
        event_effect = impact if name == target_company else 0
        change = random.uniform(-vola, vola) + event_effect - (curr_p - 500) * 0.0001
        new_p = max(1.0, curr_p * (1 + change))
        st.session_state.prices[name].append(new_p)
        if len(st.session_state.prices[name]) > 30:
            st.session_state.prices[name].pop(0)

# --- メイン画面表示 ---
st.title(f"💹 Asset Simulator ({CURRENCY})")
st.info(f"📅 日付: {st.session_state.date.strftime('%Y年%m月%d日')} \n\n {st.session_state.news}")

total_stock_val = sum(st.session_state.prices[name][-1] * st.session_state.holds[name] for name in st.session_state.companies)
total_assets = st.session_state.cash + total_stock_val

col_a, col_b = st.columns(2)
col_a.metric("Total Assets", f"{int(total_assets):,} {CURRENCY}")
col_b.metric("Cash on Hand", f"{int(st.session_state.cash):,} {CURRENCY}")
st.divider()

for name in st.session_state.companies:
    price_list = st.session_state
