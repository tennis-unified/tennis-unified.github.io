---
title: "Bài 180: Kiểm Toán Sinh Cơ Học Bước Chân — Lập Bản Đồ Mô Hình Chuyển Động Qua Phân Tích Video"
description: "Kiểm toán ba góc, hiệu chỉnh video chuyển khiệu nại chuyển động mơ hồ thành split offset đo được, tỷ lệ phục hồi và phân bố tư thế."
locale: vi
pillar: 2
article_id: 180
tags: [footwork, audit, video]
status: published
---

# BÀI 180: Kiểm Toán Sinh Cơ Học Bước Chân — Lập Bản Đồ Mô Hình Chuyển Động Qua Phân Tích Video

## Tóm Tắt Điều Hành
Kiểm toán bước chân chuyển video trận thành bản đồ chuyển động. Ba góc camera, một vài kích thước sân hiệu chỉnh và phiên mã 30 phút chuyển "di chuyển muộn" thành "split đáp 180 ms sau tiếp xúc trên 7 trong 10 rally backhand" — lỗi đo được với lệnh sửa đo được.

## Tối Thiểu Ba Góc

Mỗi góc trả lời câu hỏi khác; kiểm toán nghiêm trọng cần cả ba.

- **Cạnh** (camera 1.2-1.5 m cao, ngang người chời, 8-10 m ngoài sân): thời gian split, góc gối khi đáp, chiều dài bước, khởi động backswing so với chuyển động.
- **Phía sau** (từ đường cuối xa, trung tâm): loại bước đầu, định hướng hông khi tiếp xúc, khoảng cách ngang, đường phục hồi.
- **Rộng hoặc cao** (tripod cao, ban công, hoặc vị trí nâng 4-5 m phía sau): hình học sân — độ sâu khi tiếp xúc, điểm nhắm phục hồi.

## Hiệu Chỉnh: Sân Như Thước

Mỗi sân mang theo thước đo riêng. Kích thước biết đường cuối đến đường giao bóng 5.49 m, đường giao bóng đến lưới 6.40 m, chiều rộng đơn 8.23 m — chuyển bất kỳ khung chứa các đường đó thành chuyển đổi pixel-mét.

## Phiên Mã

Lấy mẫu 8-12 rally hoặc 30-50 cú mỗi tình huống. Bảy khung chính mỗi cú:

1. Tiếp xúc đối thủ (t = 0).
2. Đáp split của người chời, ghi là offset ms.
3. Khởi động và loại bước đầu.
4. Khởi động xoay thân.
5. Tiếp xúc người chời — vùng tư thế, độ sâu, chiều cao tiếp xúc.
6. Vị trí 0.5 s sau tiếp xúc.
7. Vị trí hoàn thành phục hồi.

## Xây Dựng Danh Sách Ưu Tiên Lỗi

Xếp hạng lỗi theo **tần số × chi phí**. Quy tắc cho danh sách:

- **Ba mục tối đa.** Danh sách mười mục không tạo gì.
- **Một lỗi mỗi lúc**, tấn công với khối sửa chữa đơn.
- **Tách kỹ thuật khỏi thể lực.** Split đúng lúc set một và muộn set ba không phải lỗi thời gian — đó là lỗi điều kiện.

## Ứng Dụng Thực Tế: "Kiểm Toán 45 Phút"
Quay 15 phút điểm từ cạnh và phía sau ở 120 fps, nâng nếu có. Mã mười cú mỗi tình huống — bảy khung, năm số liệu — vào bảng tính. Sản xuất đúng ba lỗi xếp hạng với số liệu đi kèm ("split +180 ms trên 7/10 backhand" đánh bại "di chuyển muộn"). Gán một khối sửa chữa cho lỗi hàng đầu, lên lịch kiểm toán lại cho tuần năm trên cùng góc.