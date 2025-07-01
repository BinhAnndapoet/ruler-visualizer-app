import streamlit as st
import matplotlib.pyplot as plt
import time

# --- Cấu hình trang Streamlit ---
st.set_page_config(
    page_title="Visual Hóa Bài Toán Vạch Thước",
    page_icon="📏",
    layout="wide"
)

# --- Phần lõi thuật toán (Divide and Conquer) ---

def draw_ruler_recursive(left, right, height, all_ticks):
    """
    Hàm đệ quy để tính toán vị trí và chiều cao của các vạch.
    Đây là phiên bản để thu thập tất cả các vạch cho việc vẽ tĩnh.

    Args:
        left (float): Điểm bắt đầu của đoạn thước hiện tại.
        right (float): Điểm kết thúc của đoạn thước hiện tại.
        height (int): Chiều cao của vạch ở giữa đoạn này.
        all_ticks (list): Danh sách để lưu trữ các vạch (vị trí, chiều cao).
    """
    # Điều kiện dừng: Khi chiều cao vạch <= 0, không vẽ nữa.
    if height <= 0:
        return

    # 1. Conquer (Trị): Vẽ vạch ở giữa đoạn hiện tại.
    mid = left + (right - left) / 2
    all_ticks.append((mid, height))

    # 2. Divide (Chia): Gọi đệ quy cho 2 nửa trái và phải.
    # Chiều cao vạch ở các bước tiếp theo giảm đi 1.
    draw_ruler_recursive(left, mid, height - 1, all_ticks)
    draw_ruler_recursive(mid, right, height - 1, all_ticks)


def draw_ruler_generator(left, right, height):
    """
    Hàm đệ quy sử dụng generator để "yield" từng vạch một.
    Dùng cho việc visualize từng bước (hoạt ảnh).
    """
    if height <= 0:
        return

    # 1. Conquer: Tính toán và yield vạch ở giữa trước.
    mid = left + (right - left) / 2
    yield (mid, height)

    # 2. Divide: Yield tất cả các vạch từ nửa bên trái...
    yield from draw_ruler_generator(left, mid, height - 1)
    # ...sau đó yield tất cả các vạch từ nửa bên phải.
    yield from draw_ruler_generator(mid, right, height - 1)


# --- Hàm vẽ (sử dụng Matplotlib) ---

def plot_ruler(ticks, length, max_h, title=""):
    """
    Hàm để vẽ cây thước và các vạch đã được tính toán.

    Args:
        ticks (list): Danh sách các vạch (vị trí, chiều cao).
        length (int): Tổng chiều dài của cây thước.
        max_h (int): Chiều cao vạch lớn nhất để định tỷ lệ trục Y.
        title (str): Tiêu đề cho biểu đồ.
    """
    fig, ax = plt.subplots(figsize=(12, 3))
    
    # Vẽ đường ngang của thước
    ax.plot([0, length], [0, 0], color='black', linewidth=3, zorder=1)

    # Vẽ các vạch
    if ticks:
        for x, h in ticks:
            ax.plot([x, x], [0, h], color='saddlebrown', linewidth=2, zorder=2)

    # Căn chỉnh và làm đẹp biểu đồ
    ax.set_title(title, fontsize=16)
    ax.set_xlim(-length * 0.02, length * 1.02)
    ax.set_ylim(-max_h * 0.2, max_h * 1.2)
    
    # Ẩn các trục và đường viền không cần thiết
    ax.get_yaxis().set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_position('zero')
    ax.tick_params(axis='x', which='major', labelsize=12, pad=10) # Tăng khoảng cách label trục x

    plt.tight_layout()
    return fig


# --- Giao diện người dùng Streamlit ---

st.title("📏 Visual Hóa Bài Toán Vạch Thước")
st.markdown(
    """
    Ứng dụng này minh họa giải pháp cho **Bài toán Vạch thước** bằng thuật toán **Chia để Trị (Divide and Conquer)**.
    - **Ý tưởng:** Tại mỗi bước, ta vẽ một vạch ở giữa đoạn thước hiện tại, sau đó giải quyết hai bài toán con nhỏ hơn ở hai bên (với chiều cao vạch giảm đi 1).
    - **Divide (Chia):** Chia đoạn thước `[left, right]` thành hai đoạn con `[left, mid]` và `[mid, right]`.
    - **Conquer (Trị):** Vẽ một vạch tại `mid` với chiều cao `h`.
    - **Combine (Kết hợp):** Không có bước kết hợp tường minh. Kết quả là tập hợp tất cả các vạch được vẽ trong quá trình đệ quy.
    """
)

st.sidebar.header("Tùy chọn")
ruler_length = st.sidebar.slider("Độ dài thước (L)", min_value=16, max_value=256, value=128, step=16)
max_height = st.sidebar.slider("Chiều cao vạch lớn nhất (h)", min_value=1, max_value=10, value=5)
animation_speed = st.sidebar.select_slider(
    "Tốc độ hoạt ảnh",
    options=[0.05, 0.1, 0.25, 0.5, 1.0],
    value=0.25,
    format_func=lambda x: f"{x}s"
)

col1, col2 = st.columns(2)

with col1:
    st.header("1. Vẽ Tĩnh (Kết quả cuối cùng)")
    if st.button("Vẽ kết quả cuối cùng", key="static_draw"):
        with st.spinner("Đang tính toán và vẽ thước..."):
            all_ticks = []
            draw_ruler_recursive(0, ruler_length, max_height, all_ticks)
            fig = plot_ruler(all_ticks, ruler_length, max_height, f"Thước L={ruler_length}, h={max_height}")
            st.pyplot(fig)
            st.success(f"Đã vẽ xong! Tổng cộng có {len(all_ticks)} vạch.")

with col2:
    st.header("2. Vẽ Từng Bước (Hoạt ảnh)")
    if st.button("Bắt đầu hoạt ảnh", key="animated_draw"):
        st.info(f"Bắt đầu visualize với tốc độ {animation_speed}s mỗi bước...")
        
        # Tạo một placeholder để cập nhật biểu đồ
        plot_placeholder = st.empty()
        
        # Danh sách để tích lũy các vạch đã được vẽ
        accumulated_ticks = []
        
        # Lấy generator
        tick_generator = draw_ruler_generator(0, ruler_length, max_height)
        
        step = 0
        for new_tick in tick_generator:
            step += 1
            accumulated_ticks.append(new_tick)
            
            # Vẽ lại biểu đồ với các vạch đã tích lũy
            fig = plot_ruler(
                accumulated_ticks, 
                ruler_length, 
                max_height, 
                f"Bước {step}: Vẽ vạch tại x={new_tick[0]:.2f}, cao={new_tick[1]}"
            )
            
            # Cập nhật placeholder
            plot_placeholder.pyplot(fig)
            plt.close(fig) # Giải phóng bộ nhớ
            
            # Dừng một chút để tạo hiệu ứng hoạt ảnh
            time.sleep(animation_speed)

        st.success(f"Hoạt ảnh hoàn tất sau {step} bước!")

# Thêm phần giải thích về code
with st.expander("Xem mã nguồn của thuật toán"):
    st.code("""
def draw_ruler_generator(left, right, height):
    \"\"\"
    Hàm đệ quy sử dụng generator để "yield" từng vạch một.
    Dùng cho việc visualize từng bước (hoạt ảnh).
    \"\"\"
    # Điều kiện dừng
    if height <= 0:
        return

    # 1. Conquer: Tính toán và "vẽ" vạch ở giữa
    mid = left + (right - left) / 2
    yield (mid, height) # Yield vạch này để visualize

    # 2. Divide: Gọi đệ quy cho 2 bài toán con
    # Dùng 'yield from' để tiếp tục yield các kết quả từ hàm đệ quy con
    yield from draw_ruler_generator(left, mid, height - 1)
    yield from draw_ruler_generator(mid, right, height - 1)
    """, language="python")