import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="🐎 마권연구소 v5.0", layout="wide")

# 2. 인증 정보 (파일 없이 코드에 직접 입력)
KEY_INFO = {
    "type": "service_account",
    "project_id": "ghwkdwjd",
    "private_key_id": "5779f346955f28a1c7770d19d550568f964ac5be",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCmq4VD6iLja0g3\nXCkp4nBGbhm9OsMq/f0LOyn0gXarijjmEdLOdD8fDpRyQd7xEiil92GCr457xOQq\nPP+gZAj5tP84D1+X+ldRYsBBRj0wPCFEcqAbq91jR5KAR9RZvTZlEtUxP1NAgjZt\nsfEd5309hmL6PmbbjFL+fcWYo+7MvquXwzz/Z53CfxKU8lZdLvlbctvuxalRdn/X\nzeRujFxj+ae2vSUacCY+ukhWthU3Sfwg7wgHmgj7oNEg64U4Kw1ste/gGRekmt3Z\nnSBknEFPNNOhtsAXZjfHh3URQUlGhctfrurfFxs29SDLYLgUxGsttrd5InG8p/U1\npxNZUmZ3AgMBAAECggEACmz1P5vQReCKmmfp7URMWKN/ea5I0hIkN4UiaTiF91IE\noCOiR6bO4f7z+zeynerQXx1b3KRlqclVqmy5YsuPIiuXwWZ4yNVwi9c9BnhB0Jga\nTqFK8aAtD45FFEAqANkMo4LrkhKPfxwGEpOMbR3zYBtdaqDnpzkeYev1JcivYeA7\nlufg++SmbQKAQQ1AiOllR8W3oxgoCzozZ0qHWwhIcZ+vT5ULGWq4Pn9R5WBp8Dk+\ncMoSu2BUk2Om0P2spTHWlh5fp/he0z6KB+phhCLVqYxasgg8jKxWdBEIS7+LH7Jl\nrd24gCEGVtImgFCoiZXae61hlkJQ8EgwF05D2NrBrQKBgQDXnTDpfWi/e1B1R1iI\nUI5ALrYLd7S2UH8EJsBJ1r+WOz1twXebq/io9h5tw5vDrSqGzysnc4cAtwNV6Cf+\nW1MbiyjvUs03I/0zLiYM5NAxbmldys7l9ekuM1FmeVsPH4lUtycS8eh7nHeBfKDI\nOh/ikYWhhl9svTEaWQvHkb5+6wKBgQDF42/kzdwgxhQG5ahxdkK6qbmCoxqerUXg\ncyQ7S6s14cmwDyo0ga4uvlEUo0HT22rCOGk0Ep5ajxmMyqPDoaUofktahB117hfj\nh8BMkwo9gLA35kWUUjQvfXNDZ9tOlquyT0T4sGuCy0Me82Fe5nOyMppasXrZn2HZ\nfQKCwaOLpQKBgAWoonf+Spl76wio7rHlK1aT40M5yQxf4HWDbtiBQlX3CA2xXio/\nwS7uBq5qy9O+37baCQ/oAEsMgpHmneYXD39Rj6l4Stp/n02QkH8WIkCp3SoRAI0Y\nfx4vSpud473p3fjTNbtRjgBwgtJrKu0WWW/g0dkDZc28yWUfoSeDs7QxAoGAeAyH\n/xhb6I4B7EU6sMp7pN3+KqBkL8sSTx3K5yX6kc+OGX65rezWDIlsisaX0ryTwYuT\nVwHMi0ewylbMjovrs+saL6libf6pA2GBaXLyjWkafm712wsbmYvTdxr0UnLZamzo\nfK4aKtjAuXAQrA/GNF66gTaWPpuQMu7BrS1n1/kCgYBQz88QQNvEt8X1FeyjQRL7\n2aBBSvqWwV1nWklvRIMY1EOajSeN39ouHakszGjmxiU2rkpr4cbLa/1xjXIvT6mi\ndo/BwzNbmfiDQudzPg/zrDPURvmUcFEHGo/mLISmfb0thaWFICtCPEq2TWW5I+2m\nGM0BZa7Kzl1iVqLZ5LXRbw==\n-----END PRIVATE KEY-----\n",
    "client_email": "ghwkdwjd@ghwkdwjd.iam.gserviceaccount.com",
    "client_id": "115862792259224573682",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ghwkdwjd%40ghwkdwjd.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# 3. 데이터 로드 함수
def load_data():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        # 코드 안의 KEY_INFO로 즉시 인증
        creds = Credentials.from_service_account_info(KEY_INFO, scopes=scope)
        client = gspread.authorize(creds)
        
        # 구글 시트 ID 연결
        sh = client.open_by_key("1UpSdWIIlmFKRJgN3GfZdRUVUHd-TlPXyZLG3JUxQVFk")
        data = sh.worksheet("부산").get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"⚠️ 연결 실패: {e}")
        return pd.DataFrame()

# 4. 화면 구성
st.title("🐎 부산 경마 출전표")

df = load_data()

if not df.empty:
    st.success("✅ 연결 성공!")
    st.dataframe(df, use_container_width=True)
else:
    st.info("시트에 데이터가 없
