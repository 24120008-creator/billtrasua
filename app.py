import streamlit as st
from datetime import datetime
from pathlib import Path

# ============================================================
# CẤU HÌNH TRANG
# ============================================================

st.set_page_config(
    page_title="Quán Trà Sữa",
    page_icon="🧋",
    layout="centered"
)

# ============================================================
# THÔNG TIN QUÁN
# ============================================================

TEN_QUAN = "QUÁN TRÀ SỮA"
DIA_CHI = "109 Bình Dương"
TEN_LOGO = "logo3.jpg"

# ============================================================
# ẢNH NỀN logo3.jpg
# ============================================================

logo_path = Path(TEN_LOGO)

if logo_path.exists():

    # Đọc ảnh để tạo background
    import base64

    with open(logo_path, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image:
                linear-gradient(
                    rgba(255,255,255,0.88),
                    rgba(255,255,255,0.88)
                ),
                url("data:image/jpeg;base64,{encoded_image}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .main {{
            padding-top: 1rem;
        }}

        .title-box {{
            background-color: rgba(255,255,255,0.92);
            padding: 20px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 20px;
        }}

        .bill-box {{
            background-color: rgba(255,255,255,0.95);
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #ddd;
        }}

        .chat-box {{
            background-color: rgba(255,255,255,0.95);
            padding: 15px;
            border-radius: 15px;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

else:

    st.warning(
        "⚠️ Không tìm thấy file logo3.jpg. "
        "Hãy đặt logo3.jpg cùng thư mục với app.py."
    )

# ============================================================
# LOGO
# ============================================================

if logo_path.exists():
    st.image(
        TEN_LOGO,
        use_container_width=True
    )

# ============================================================
# TIÊU ĐỀ
# ============================================================

st.markdown(
    """
    <div class="title-box">
        <h1>🧋 QUÁN TRÀ SỮA</h1>
        <h3>HỆ THỐNG TÍNH HÓA ĐƠN</h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(f"📍 Địa chỉ quán: {DIA_CHI}")

st.markdown("---")

# ============================================================
# MENU THỨC UỐNG
# ============================================================

MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa trân châu đường đen": 35000,
    "Trà đào": 28000,
    "Trà vải": 28000,
    "Matcha Latte": 42000,
    "Trà chanh": 25000,
    "Trà tắc": 25000
}

# ============================================================
# GIÁ SIZE
# ============================================================

SIZE_PRICE = {
    "S": 0,
    "M": 5000,
    "L": 10000
}

# ============================================================
# TOPPING
# ============================================================

TOPPINGS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 7000,
    "Pudding": 8000,
    "Kem cheese": 10000
}

# ============================================================
# THÔNG TIN KHÁCH HÀNG
# ============================================================

st.subheader("👤 Thông tin khách hàng")

customer_name = st.text_input(
    "👤 Tên khách hàng",
    placeholder="Nhập tên khách hàng"
)

phone = st.text_input(
    "📱 Số điện thoại",
    placeholder="Nhập số điện thoại"
)

# ============================================================
# CHỌN NHIỀU MÓN
# ============================================================

st.markdown("---")
st.subheader("🥤 Chọn thức uống")

selected_drinks = st.multiselect(
    "Bạn có thể chọn nhiều món cùng lúc:",
    list(MENU.keys())
)

drink_quantities = {}
drink_sizes = {}

# ============================================================
# THÔNG TIN TỪNG MÓN
# ============================================================

if selected_drinks:

    st.write("### 📋 Thông tin từng món")

    for drink in selected_drinks:

        st.markdown(f"#### 🥤 {drink}")

        col1, col2 = st.columns(2)

        with col1:

            drink_quantities[drink] = st.number_input(
                f"🔢 Số lượng",
                min_value=1,
                max_value=50,
                value=1,
                step=1,
                key=f"quantity_{drink}"
            )

        with col2:

            drink_sizes[drink] = st.selectbox(
                f"📏 Size",
                ["S", "M", "L"],
                key=f"size_{drink}"
            )

        st.caption(
            f"Giá gốc: {MENU[drink]:,} VNĐ | "
            f"Size {drink_sizes[drink]}: "
            f"+{SIZE_PRICE[drink_sizes[drink]]:,} VNĐ"
        )

# ============================================================
# MỨC ĐƯỜNG
# ============================================================

st.markdown("---")
st.subheader("🍬 Mức độ đường")

sugar = st.selectbox(
    "Chọn mức đường",
    [
        "100%",
        "70%",
        "50%",
        "30%",
        "0%"
    ]
)

# ============================================================
# MỨC ĐÁ
# ============================================================

st.subheader("🧊 Mức độ đá")

ice = st.selectbox(
    "Chọn mức đá",
    [
        "100%",
        "70%",
        "50%",
        "30%",
        "0% - Không đá"
    ]
)

# ============================================================
# TOPPING
# ============================================================

st.markdown("---")
st.subheader("➕ Chọn topping")

selected_toppings = st.multiselect(
    "Có thể chọn nhiều topping:",
    list(TOPPINGS.keys())
)

# ============================================================
# TÍNH TIỀN
# ============================================================

total = 0

drink_details = []

for drink in selected_drinks:

    size = drink_sizes[drink]
    quantity = drink_quantities[drink]

    unit_price = (
        MENU[drink]
        + SIZE_PRICE[size]
    )

    subtotal = unit_price * quantity

    total += subtotal

    drink_details.append(
        {
            "name": drink,
            "size": size,
            "quantity": quantity,
            "unit_price": unit_price,
            "subtotal": subtotal
        }
    )

# ============================================================
# TÍNH TIỀN TOPPING
# ============================================================

topping_price = 0

for topping in selected_toppings:
    topping_price += TOPPINGS[topping]

total += topping_price

# ============================================================
# ĐIỂM TÍCH LŨY
# ============================================================

points = total // 10000

# ============================================================
# HÓA ĐƠN
# ============================================================

st.markdown("---")
st.subheader("🧾 HÓA ĐƠN")

st.markdown(
    '<div class="bill-box">',
    unsafe_allow_html=True
)

st.write(f"🏪 **{TEN_QUAN}**")
st.write(f"📍 **Địa chỉ:** {DIA_CHI}")

if customer_name:
    st.write(f"👤 **Khách hàng:** {customer_name}")
else:
    st.write("👤 **Khách hàng:** Chưa nhập")

if phone:
    st.write(f"📱 **Số điện thoại:** {phone}")
else:
    st.write("📱 **Số điện thoại:** Chưa nhập")

st.markdown("---")

# ============================================================
# DANH SÁCH MÓN
# ============================================================

if selected_drinks:

    for item in drink_details:

        st.write(
            f"🥤 **{item['name']}**"
        )

        st.write(
            f"   Size {item['size']} × "
            f"{item['quantity']} ly × "
            f"{item['unit_price']:,} VNĐ"
        )

        st.write(
            f"   ➜ Thành tiền: "
            f"**{item['subtotal']:,} VNĐ**"
        )

else:

    st.info("Chưa chọn thức uống.")

# ============================================================
# ĐƯỜNG - ĐÁ
# ============================================================

st.markdown("---")

st.write(f"🍬 **Mức đường:** {sugar}")
st.write(f"🧊 **Mức đá:** {ice}")

# ============================================================
# TOPPING
# ============================================================

if selected_toppings:

    st.write("➕ **Topping:**")

    for topping in selected_toppings:

        st.write(
            f"• {topping}: "
            f"{TOPPINGS[topping]:,} VNĐ"
        )

else:

    st.write("➕ **Topping:** Không")

# ============================================================
# TỔNG TIỀN
# ============================================================

st.markdown("---")

st.success(
    f"💰 TỔNG TIỀN: {total:,} VNĐ"
)

st.info(
    f"⭐ ĐIỂM TÍCH LŨY: {points} điểm"
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# CHATBOT
# ============================================================

st.markdown("---")

st.subheader("🤖 Chatbot hỗ trợ khách hàng")

st.write(
    "Bạn có thể hỏi chatbot về địa chỉ, size, topping, "
    "giờ mở cửa hoặc giá món."
)

question = st.text_input(
    "💬 Nhập câu hỏi:",
    placeholder="Ví dụ: Quán có những size nào?"
)

if question:

    q = question.lower().strip()

    # --------------------------------------------
    # ĐỊA CHỈ
    # --------------------------------------------

    if (
        "địa chỉ" in q
        or "ở đâu" in q
        or "địa điểm" in q
    ):

        st.success(
            f"📍 Quán có địa chỉ tại: {DIA_CHI}"
        )

    # --------------------------------------------
    # GIỜ MỞ CỬA
    # --------------------------------------------

    elif (
        "giờ mở cửa" in q
        or "mở cửa" in q
        or "đóng cửa" in q
        or "mấy giờ" in q
    ):

        st.success(
            "⏰ Quán mở cửa từ 07:00 đến 22:00 mỗi ngày."
        )

    # --------------------------------------------
    # SIZE
    # --------------------------------------------

    elif (
        "size" in q
        or "kích thước" in q
        or "cỡ" in q
    ):

        st.success(
            "🥤 Quán có 3 size: "
            "S, M và L. "
            "Size M cộng 5.000 VNĐ, "
            "size L cộng 10.000"
        )
