# ruler-visualizer-app

# 📏 Visual Hóa Bài Toán Vạch Thước (Ruler Drawing Problem Visualizer)

## 🚀 Link truy cập ứng dụng
**[https://your-app-link.streamlit.app](https://ruler-drawing-demo.streamlit.app/)**

## 📜 Mô tả bài toán

Bài toán Vạch Thước được mô tả như sau:

> Cho một cây thước có độ dài `L` và một chiều cao vạch lớn nhất `h`. Hãy vẽ các vạch trên thước theo quy tắc đệ quy sau:
> 1.  Vẽ một vạch có chiều cao `h` ở chính giữa cây thước.
> 2.  Với mỗi nửa còn lại của cây thước, lặp lại quy trình trên với chiều cao vạch giảm đi 1 (`h-1`).
> 3.  Quá trình dừng lại khi chiều cao vạch bằng 0.

Kết quả sẽ là một cây thước quen thuộc với các vạch dài ở giữa, và các vạch ngắn dần khi chia nhỏ các khoảng.

## 💡 Ý tưởng giải quyết: Chia để Trị (Divide and Conquer)

Thuật toán Chia để Trị là một cách tiếp cận tự nhiên và thanh lịch để giải quyết bài toán này. Ý tưởng được chia thành ba bước:

1.  **Divide (Chia):** Tại mỗi bước, chia đoạn thước `[left, right]` hiện tại thành hai đoạn con bằng nhau: `[left, mid]` và `[mid, right]`, với `mid` là điểm giữa.

2.  **Conquer (Trị):** Giải quyết "bài toán" đơn giản nhất tại bước hiện tại: vẽ một vạch tại điểm `mid` với chiều cao `h` tương ứng.

3.  **Combine (Kết hợp):** Gọi đệ quy để giải quyết hai bài toán con trên hai đoạn `[left, mid]` và `[mid, right]` với chiều cao vạch được giảm đi 1 (`h-1`). Trong bài toán này, bước kết hợp không tường minh; kết quả cuối cùng là tập hợp của tất cả các vạch được vẽ trong toàn bộ quá trình đệ quy.

Hàm đệ quy sẽ có dạng như sau:
```python
def draw_ruler(left, right, height):
    # Điều kiện dừng
    if height <= 0:
        return

    # Conquer: Vẽ vạch ở giữa
    mid = (left + right) / 2
    draw_tick(mid, height)

    # Divide: Gọi đệ quy cho 2 nửa
    draw_ruler(left, mid, height - 1)
    draw_ruler(mid, right, height - 1)
