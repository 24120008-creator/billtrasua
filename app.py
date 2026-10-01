import streamlit as st

from datetime import datetime

import sqlite3
st.image("logo3.jpg")

# =========================================================

# CẤU HÌNH

# =========================================================

st.set_page_config(

    page_title="Quán Trà Sữa",

    page_icon="🧋",

    layout="centered"

)

# =========================================================

# KẾT NỐI DATABASE TÍCH ĐIỂM

# =========================================================

conn = sqlite3.connect(

    "tich_diem.db",

    check_same_thread=False

)

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS khach_hang (

    so_dien_thoai TEXT PRIMARY KEY,

    ten_khach TEXT,

    diem INTEGER DEFAULT 0

)

""")

conn.commit()

# =========================================================

# THÔNG TIN QUÁN

# =========================================================

TEN_QUAN = "🧋 QUÁN TRÀ SỮA"

DIA_CHI = "📍 Lê Hồng Phong, Phú Lợi"

# =========================================================

# MENU TRÀ SỮA

# =========================================================

MENU = {

    "Trà sữa truyền thống": 30000,

    "Trà sữa matcha": 35000,

    "Trà sữa socola": 35000,

    "Trà sữa dâu": 35000,

    "Trà sữa khoai môn": 38000,

    "Trà sữa caramel": 38000,

    "Trà đào": 30000,

    "Trà vải": 30000,

    "Trà chanh": 25000

}

# =========================================================

# SIZE

# =========================================================

SIZE = {

    "S": 0,

    "M": 5000,

    "L": 10000

}

# =========================================================

# TOPPING

# =========================================================

TOPPINGS = {

    "Không topping": 0,

    "Trân châu đen": 5000,

    "Trân châu trắng": 5000,

    "Thạch trái cây": 5000,

    "Pudding trứng": 7000,

    "Kem cheese": 8000,

    "Trân châu hoàng kim": 7000

}

# =========================================================

# SESSION STATE

# =========================================================

if "cart" not in st.session_state:

    st.session_state.cart = []

if "payment_done" not in st.session_state:

    st.session_state.payment_done = False

if "invoice" not in st.session_state:

    st.session_state.invoice = ""

if "points_earned" not in st.session_state:

    st.session_state.points_earned = 0

if "total_points" not in st.session_state:

    st.session_state.total_points = 0

if "messages" not in st.session_state:

    st.session_state.messages = []

# =========================================================

# HÀM LẤY ĐIỂM

# =========================================================

def lay_diem(so_dien_thoai):

    cursor.execute(

        """

        SELECT diem

        FROM khach_hang

        WHERE so_dien_thoai = ?

        """,

        (so_dien_thoai,)

    )

    result = cursor.fetchone()

    if result:

        return result[0]

    return 0

# =========================================================

# TIÊU ĐỀ

# =========================================================

st.title(TEN_QUAN)

st.write(

    f"**{DIA_CHI}**"

)

st.subheader("🧾 TÍNH HÓA ĐƠN")

st.divider()

# =========================================================

# THÔNG TIN KHÁCH HÀNG

# =========================================================

st.header("👤 Thông tin khách hàng")

ten_khach = st.text_input(

    "Tên khách hàng",

    placeholder="Nhập tên khách hàng..."

)

so_dien_thoai = st.text_input(

    "📱 Số điện thoại",

    placeholder="Nhập số điện thoại 10 số...",

    max_chars=10

)

diem_hien_tai = 0

if so_dien_thoai:

    if (

        so_dien_thoai.isdigit()

        and len(so_dien_thoai) == 10

    ):

        diem_hien_tai = lay_diem(

            so_dien_thoai

        )

        st.success(

            f"⭐ Khách hàng hiện có: "

            f"**{diem_hien_tai} điểm**"

        )

    elif not so_dien_thoai.isdigit():

        st.warning(

            "⚠️ Số điện thoại chỉ được nhập số!"

        )

    elif len(so_dien_thoai) != 10:

        st.warning(

            "⚠️ Số điện thoại phải có 10 số!"

        )

st.divider()

# =========================================================

# CHỌN NHIỀU MÓN

# =========================================================

st.header("🧋 Chọn món")

st.write(

    "Bạn có thể chọn **nhiều loại trà sữa cùng lúc**:"

)

danh_sach_mon = st.multiselect(

    "Chọn loại trà sữa",

    list(MENU.keys()),

    placeholder="Chọn một hoặc nhiều món..."

)

# =========================================================

# CẤU HÌNH TỪNG MÓN

# =========================================================

cac_mon_da_chon = []

if danh_sach_mon:

    st.subheader("⚙️ Tùy chỉnh từng món")

    for index, mon in enumerate(danh_sach_mon):

        with st.container(border=True):

            st.markdown(

                f"### 🧋 {index + 1}. {mon}"

            )

            # =================================================

            # SIZE

            # ==============
