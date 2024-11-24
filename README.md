# Game Xếp Số 35-Puzzle

Game xếp số 6x6 (35 số) với giao diện web sử dụng Flask và Bootstrap 5. Người chơi cần sắp xếp các số từ 1-35 theo thứ tự, với ô trống ở vị trí cuối cùng.

## Yêu cầu hệ thống

- Python 3.x
- pip (Python package installer)
- Trình duyệt web hiện đại (Chrome, Firefox, Edge...)
- Kết nối internet (để tải Bootstrap và các thư viện)

## Cài đặt

1. Clone repository hoặc tải source code về máy:
```bash
git https://github.com/huydepzai2810/puzzle66.git
cd puzzle66
```

2. Tạo và kích hoạt môi trường ảo (khuyến nghị):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

## Cấu trúc thư mục
```
puzzle66/
│
├── app.py              # Server Flask và logic game
├── templates/          # Thư mục chứa template
│   └── index.html     # Giao diện web
├── requirements.txt    # Danh sách thư viện cần thiết
└── README.md          # File hướng dẫn
```

## Cách chạy

1. Đảm bảo bạn đang ở thư mục gốc của project và môi trường ảo đã được kích hoạt

2. Chạy server Flask:
```bash
pip install flask
py app.py
```

3. Mở trình duyệt web và truy cập:
```
http://localhost:5000
```

## Cách chơi

1. Click "Start Game" để bắt đầu trò chơi
2. Di chuyển các ô số bằng cách click vào ô cạnh ô trống
3. Sắp xếp các số từ 1-35 theo thứ tự từ trái qua phải, trên xuống dưới
4. Ô trống phải ở vị trí cuối cùng (góc phải dưới)
5. Game kết thúc khi tất cả các số được sắp xếp đúng vị trí

## Các tính năng

- Đếm thời gian chơi (phút:giây)
- Đếm số bước di chuyển
- Tự động giải (Auto Solve) sử dụng thuật toán A*
- Reset game để chơi lại
- Kiểm tra chiến thắng tự động
- Hiển thị thời gian hoàn thành
- Tips hiển thị hướng dẫn chơi
- Responsive design (chơi được trên mobile)

## Các nút điều khiển

- Start Game: Bắt đầu game mới
- Auto Solve: Tự động giải
- Reset: Chơi lại từ đầu
- Phím R: Reset game nhanh

## Công nghệ sử dụng

### Backend
- Python 3.x
- Flask framework
- Thuật toán A* cho tự động giải

### Frontend
- HTML5
- CSS3
- JavaScript (ES6+)
- Bootstrap 5
- Fetch API

## Xử lý lỗi thường gặp

1. Lỗi "ModuleNotFoundError: No module named 'flask'":
```bash
pip install flask
```

2. Lỗi "Address already in use":
```python
# Thay đổi port trong app.py
if __name__ == '__main__':
    app.run(debug=True, port=5001)
```

3. Lỗi không tìm thấy template:
```bash
# Kiểm tra cấu trúc thư mục
ls templates/
```

## Thuật toán A* (Auto Solve)

Thuật toán A* được sử dụng để tự động giải puzzle với:
- Heuristic: Manhattan distance
- Cost function: f(n) = g(n) + h(n)
  - g(n): số bước di chuyển từ trạng thái ban đầu
  - h(n): tổng khoảng cách Manhattan của các số đến vị trí đích

## Tối ưu hiệu năng

### Server
- Cache các trạng thái đã duyệt
- Giới hạn số bước tìm kiếm (7000 bước)
- Tối ưu hóa hàm heuristic

### Client
- Sử dụng CSS transitions cho animation
- Tối ưu render board với DOM manipulation
- Debounce các event handler

## Phát triển thêm

Các tính năng có thể phát triển:
1. Lưu điểm cao
2. Nhiều cấp độ khó
3. Chế độ multiplayer
4. Thêm âm thanh
5. Thêm hiệu ứng đẹp hơn

## Đóng góp

Mọi đóng góp đều được hoan nghênh! Hãy:
1. Fork repository
2. Tạo branch mới
3. Commit changes
4. Push to branch
5. Tạo Pull Request
