import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 1. 페이지 설정 및 모바일 디자인 (CSS)
st.set_page_config(page_title="🐎 마권연구소 - 출전표", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    .race-header {
        background-color: #2c3e50;
        color: white;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .horse-card {
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        background-color: white;
        margin-bottom: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .horse-no-name {
        display: flex;
        align-items: center;
        border-bottom: 1px solid #eee;
        padding-bottom: 8px;
    }
    .horse-no {
        font-size: 24px;
        font-weight: bold;
        color: white;
        background: #e74c3c;
        padding: 0 10px;
        border-radius: 5px;
        margin-right: 15px;
    }
    .horse-name {
        font-size: 20px;
        font-weight: bold;
        color: #333;
    }
    .stat-row {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
        font-size: 16px;
        color: #555;
    }
