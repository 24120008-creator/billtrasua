import streamlit as st
from pathlib import Path
import base64
import requests

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
GIO_MO_CUA = "07:00 - 22:00 mỗi ngày"

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
# ẢNH NỀN logo3.jpg
# ============================================================

logo_path = Path(TEN_LOGO)

if logo_path.exists():

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
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #ddd;
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

st.info(
    f"📍 Địa chỉ quán: {DIA_CHI}"
)

st.markdown("---")

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
# CHỌN THỨC UỐNG
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

        st.markdown(
            f"#### 🥤 {drink}"
        )

        col1, col2 = st.columns(2)

        with col1:

            drink_quantities[drink] = st.number_input(
                "🔢 Số lượng",
                min_value=1,
                max_value=50,
                value=1,
                step=1,
                key=f"quantity_{drink}"
            )

        with col2:

            drink_sizes[drink] = st.selectbox(
                "📏 Size",
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

st.write(
    f"🏪 **{TEN_QUAN}**"
)

st.write(
    f"📍 **Địa chỉ:** {DIA_CHI}"
)

if customer_name:

    st.write(
        f"👤 **Khách hàng:** {customer_name}"
    )

else:

    st.write(
        "👤 **Khách hàng:** Chưa nhập"
    )

if phone:

    st.write(
        f"📱 **Số điện thoại:** {phone}"
    )

else:

    st.write(
        "📱 **Số điện thoại:** Chưa nhập"
    )

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
            f"Size {item['size']} × "
            f"{item['quantity']} ly × "
            f"{item['unit_price']:,} VNĐ"
        )

        st.write(
            f"➜ Thành tiền: "
            f"**{item['subtotal']:,} VNĐ**"
        )

else:

    st.info(
        "Chưa chọn thức uống."
    )

# ============================================================
# ĐƯỜNG - ĐÁ
# ============================================================

st.markdown("---")

st.write(
    f"🍬 **Mức đường:** {sugar}"
)

st.write(
    f"🧊 **Mức đá:** {ice}"
)

# ============================================================
# TOPPING
# ============================================================

if selected_toppings:

    st.write(
        "➕ **Topping:**"
    )

    for topping in selected_toppings:

        st.write(
            f"• {topping}: "
            f"{TOPPINGS[topping]:,} VNĐ"
        )

else:

    st.write(
        "➕ **Topping:** Không"
    )

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
    "</div>",
    unsafe_allow_html=True
)

# ============================================================
# CHATBOT AI
# ============================================================

st.markdown("---")

st.subheader(
    "🤖 Chatbot AI hỗ trợ khách hàng"
)

st.write(
    "Bạn có thể hỏi chatbot về menu, giá món, "
    "size, topping, mức đường, mức đá, "
    "địa chỉ hoặc giờ mở cửa."
)

# ============================================================
# LẤY API KEY TỪ STREAMLIT SECRETS
# ============================================================

try:

    API_KEY = st.secrets["OPENROUTER_API_KEY"]

except Exception:

    API_KEY = ""

# ============================================================
# HÀM GỌI OPENROUTER
# ============================================================

def ask_chatbot(question):

    if not API_KEY:

        return (
            "⚠️ Chatbot chưa được cấu hình API Key.\n\n"
            "Bạn hãy thêm OPENROUTER_API_KEY "
            "vào phần Secrets của Streamlit."
        )

    menu_text = "\n".join(
        [
            f"- {name}: {price:,} VNĐ"
            for name, price in MENU.items()
        ]
    )

    size_text = (
        "- S: không cộng thêm\n"
        "- M: +5.000 VNĐ\n"
        "- L: +10.000 VNĐ"
    )

    topping_text = "\n".join(
        [
            f"- {name}: {price:,} VNĐ"
            for name, price in TOPPINGS.items()
        ]
    )

    system_prompt = f"""
Bạn là chatbot chăm sóc khách hàng của {TEN_QUAN}.

THÔNG TIN QUÁN:

Tên quán:
{TEN_QUAN}

Địa chỉ:
{DIA_CHI}

Giờ mở cửa:
{GIO_MO_CUA}

MENU:

{menu_text}

SIZE:

{size_text}

TOPPING:

{topping_text}

MỨC ĐƯỜNG:

100%, 70%, 50%, 30%, 0%

MỨC ĐÁ:

100%, 70%, 50%, 30%, 0% - Không đá

QUY TẮC TRẢ LỜI:

1. Luôn trả lời bằng tiếng Việt.

2. Trả lời thân thiện, ngắn gọn và dễ hiểu.

3. Khi khách hỏi giá món phải sử dụng đúng
   bảng giá được cung cấp.

4. Nếu khách hỏi giá theo size,
   hãy cộng đúng giá size.

5. Nếu khách hỏi topping,
   hãy sử dụng đúng giá topping.

6. Nếu khách hỏi địa chỉ,
   trả lời địa chỉ: {DIA_CHI}

7. Nếu khách hỏi giờ mở cửa,
   trả lời: {GIO_MO_CUA}

8. Có thể tư vấn khách chọn món dựa trên
   sở thích như ngọt, ít ngọt, nhiều topping.

9. Không tự bịa món hoặc giá.

10. Nếu không có thông tin thì nói:
"Mình chưa có thông tin này, bạn vui lòng liên hệ
quán để được hỗ trợ nhé."

11. Không tiết lộ API Key hoặc thông tin kỹ thuật.
"""

    url = (
        "https://openrouter.ai/api/v1/chat/completions"
    )

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "Quán Trà Sữa"
    }

    data = {
        "model": "openrouter/free",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code != 200:

            try:

                error_data = response.json()

                error_message = (
                    error_data
                    .get("error", {})
                    .get(
                        "message",
                        "Không xác định"
                    )
                )

            except Exception:

                error_message = response.text

            return (
                "❌ Chatbot gặp lỗi:\n\n"
                f"{error_message}"
            )

        result = response.json()

        answer = (
            result["choices"][0]
            ["message"]
            ["content"]
        )

        return answer

    except requests.exceptions.Timeout:

        return (
            "⏰ Chatbot phản hồi quá lâu. "
            "Bạn hãy thử lại nhé."
        )

    except requests.exceptions.RequestException as e:

        return (
            "❌ Không thể kết nối đến chatbot.\n\n"
            f"Lỗi: {e}"
        )

    except Exception as e:

        return (
            "❌ Có lỗi xảy ra.\n\n"
            f"Lỗi: {e}"
        )


# ============================================================
# LƯU LỊCH SỬ CHAT
# ============================================================

if "chat_messages" not in st.session_state:

    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "Xin chào! 👋\n\n"
                "Mình là chatbot của Quán Trà Sữa. "
                "Bạn có thể hỏi mình về menu, giá món, "
                "size, topping, địa chỉ hoặc giờ mở cửa nhé! 🧋"
            )
        }
    ]

# ============================================================
# HIỂN THỊ LỊCH SỬ CHAT
# ============================================================

for message in st.session_state.chat_messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )

# ============================================================
# NHẬP CÂU HỎI
# ============================================================

question = st.chat_input(
    "💬 Nhập câu hỏi cho chatbot..."
)

if question:

    # Lưu câu hỏi
    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Hiển thị câu hỏi
    with st.chat_message("user"):

        st.write(question)

    # Gọi chatbot
    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 Chatbot đang trả lời..."
        ):

            answer = ask_chatbot(question)

        st.write(answer)

    # Lưu câu trả lời
    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# ============================================================
# XÓA LỊCH SỬ CHAT
# ============================================================

st.markdown("---")

if st.button(
    "🗑️ Xóa lịch sử chatbot"
):

    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "Xin chào! 👋\n\n"
                "Mình là chatbot của Quán Trà Sữa. "
                "Bạn muốn hỏi gì về menu, "
                "giá món, size hoặc topping?"
            )
        }
    ]

    st.rerun()
