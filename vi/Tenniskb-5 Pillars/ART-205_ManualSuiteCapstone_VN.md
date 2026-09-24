# ART-205: Kế Hoạch Chính — Tổng Kết Bộ Sổ Tay ( "Hệ Điều Hành" )

## Tóm Tắt Điều Hành
Các Bài 191-194 Sản Xuất Ra Bốn Tài Liệu Chính: Kế Hoạch Sự Nghiệp VĐ (CEO), Kế Hoạch Chương Trình HLV (COO), Kế Hoạch Hệ Thống Học Viện (Nhà Máy), Kế Hoạch Hỗ Trợ Cha Mẹ (Cổ Đông). Tổng Kết Này Tích Hợp Chúng Thành Một **Hệ Điều Hành Thống Nhất** — "Bộ Sổ Tay" — Với Kiểm Soát Phiên Bản, Quản Trị, Xem Xét Chéo, Và Kiến Trúc "Nguồn Sự Thật Đơn Nhất" Cho Doanh Nghiệp Hiệu Suất Cao 5 Cột Trụ.

## Kiến Trúc Bộ Sổ Tay: Một Hệ Thống, Bốn Sổ Tay

### Nguyên Lý Tích Hợp
*   **Kế Hoạch Sự Nghiệp VĐ (BÀI-191):** **Chiến Lược** (Đi Đâu & Tại Sao).
*   **Kế Hoạch Chương Trình HLV (BÀI-192):** **Vận Hành** (Cái Gì & Cách Làm).
*   **Kế Hoạch Hệ Thống Học Viện (BÀI-193):** **Cơ Sở Hạ Tầng** (Môi Trường & Dung Lượng).
*   **Kế Hoạch Hỗ Trợ Cha Mẹ (BÀI-194):** **Quản Trị** (Ranh Giới & Đầu Tư).

**Quy Tắc:** Không Sổ Tay Nào Tồn Tại Độc Lập. Mọi Thay Đổi Trong Một Kích Hoạt Xem Xét Trong Các Sổ Khác. **Kiểm Soát Phiên Bản Là Bắt Buộc.**

## Mô Hình Quản Trị Thống Nhất: "Hội Đồng"

### Thành Phần
1.  **Vận Động Viên (CEO)** — Tầm Nhìn, Giá Trị, Quyền Quyết Định Cuối Cùng.
2.  **HLV Trưởng / Giám Đốc Chương Trình (COO)** — Vận Hành, Truyền Thông, Chất Lượng.
3.  **Giám Đốc Kỹ Thuật (Học Viện)** — Cơ Sở Hạ Tầng, Chương Trình Giảng Dạy, Phát Triển HLV.
4.  **Đại Diện Cha Mẹ** — Đầu Tư, Phúc Lợi, Thực Thi Ranh Giới.
5.  **Cán Bộ Phúc Lợi Độc Lập** — Bảo Vệ, Đạo Đức, Giọng Nói VĐ.
6.  **Đại Lý/Quản Lý (Tùy Chọn)** — Thương Mại, Lịch Trình, Pháp Lý.
7.  **Giám Đốc Y Tế (Tư Vấn)** — Tự Chủ Sức Khỏe, Quyền Veto RTP.

### Nhịp Độ Họp ( "Nhịp Đập Tim" )

| Nhịp Độ | Cuộc Họp | Chủ Tịch | Tham Dự Bắt Buộc | Quyết Định Then Chốt |
| :--- | :--- | :--- | :--- | :--- |
| **Hàng Tuần** | **Stand-Up Hiệu Suất** | COO | CEO, COO | Chủ Đề Tuần. Điều Chỉnh Tải. Cờ Đỏ. |
| **Hàng Tháng** | **Xem Xét Vận Hành** | COO | CEO, COO, GĐKT, Đại Diện Cha Mẹ | Xu Hướng KPI. Thay Đổi Lịch. Cập Nhật Giao Thức. |
| **Hàng Quý** | **Hội Đồng Chiến Lược** | CEO | **Tất Cả Thành Viên Hội Đồng** | **Kết Quả Đánh Giá. Cập Nhật Sổ Tay. Ngân Sách. Thay Đổi Đội Ngũ. Xem Xét Rủi Ro.** |
| **Hàng Năm** | **Đại Hội Thường Niên** | Chủ Tịch | **Tất Cả + Đại Lý + Giám Đốc Y Tế** | **Reset Tầm Nhìn. Gia Hạn Hợp Đồng. Kiểm Toán Tài Chính. Bump Phiên Bản Bộ Sổ Tay.** |

## Hệ Thống Kiểm Soát Phiên Bản: "Git Cho Tennis"

### Cấu Trúc Kho Lưu Trữ
```
/Bo_So_Tay/
├── v1.0_YYYY/                 # Phiên Bản Chính Hàng Năm
│   ├── 191_Ke_Hoach_Su_Nghiep_VD.md
│   ├── 192_Ke_Hoach_Chuong_Trinh_HLV.md
│   ├── 193_Ke_Hoach_He_Thong_Hoc_Vien.md
│   ├── 194_Ke_Hoach_Ho_Tro_Cha_Me.md
│   └── 195_Chi_Muc_Bo_So_Tay.md
├── v1.1_Q2_YYYY/              # Phiên Bản Phụ Hàng Quý
│   └── (chỉ các file thay đổi)
├── Working_Drafts/            # Bản Nháp Đang Chỉnh Sửa
└── Archive/                   # Các Phiên Bản Cũ
```

### Giao Thức Quản Lý Thay Đổi
1.  **Đề Xuất:** Bất Kỳ Thành Viên Hội Đồng Nào Nộp "Yêu Cầu Thay Đổi" (CR) Với Lý Do, Phân Tích Tác Động, Các Sổ Tay Bị Ảnh Hưởng.
2.  **Phân Tích Tác Động:** COO + GĐKT Đánh Giá Tác Động Kỹ Thuật, Vận Hành, Tài Chính, Phúc Lợi.
3.  **Cửa Sổ Xem Xét:** 7 Ngày Cho Hội Đồng Bình Luận.
4.  **Quyết Định:** CEO Phê Duyệt / Hội Đồng Đồng Thuận (Thay Đổi Lớn).
5.  **Triển Khai:** COO Cập Nhật Sổ Tay. Bump Phiên Bản (Major.Minor.Patch).
6.  **Trao Đổi:** Nhật Ký Thay Đổi Được Phân Phối. Tóm Tắt "Đã Thay Đổi Gì" Cho VĐ/Cha Mẹ.
7.  **Lưu Trữ:** Phiên Bản Cũ Được Lưu Trữ. Chỉ Đọc.

### Quy Tắc Phiên Bản
*   **Major (vX.0):** Đại Hội Thường Niên Hàng Năm. Thay Đổi Tầm Nhìn/Chiến Lược. Cấu Trúc Sổ Tay Mới.
*   **Minor (vX.Y):** Hội Đồng Hàng Quý. Trung Chu Kỳ Mới. Thay Đổi HLV. Cập Nhật Giao Thức Lớn.
*   **Patch (vX.Y.Z):** Hàng Tuần/Hàng Tháng. Điều Chỉnh Mục Tiêu KPI. Đổi Bài Tập. Điều Chỉnh Lịch Trình.

## Ma Trận Xem Xét Chéo (Interlocking Review Matrix)

| Kích Hoạt | Kế Hoạch VĐ (191) | Kế Hoạch HLV (192) | Kế Hoạch Học Viện (193) | Kế Hoạch Cha Mẹ (194) |
| :--- | :--- | :--- | :--- | :--- |
| **Đánh Giá Hàng Quý (BÀI-118)** | Cập Nhật Mục Tiêu KPI. Kiểm Tra Tầm Nhìn. | Cập Nhật Khối Kỹ Năng. Chuyển Trục Trung Chu Kỳ. | Xem Xét Đạt Cửa Giai Đoạn. Tinh Chỉnh Chương Trình. | Xem Xét Tiến Độ Giáo Dúc. Kiểm Toán Ranh Giới. |
| **Chấn Thương / RTP (BÀI-148)** | Điều Chỉnh Dòng Thời Gian Kết Quả. | Điều Chỉnh Tải/Nội Dung Buổi Tập. | Kiểm Tra Hỗ Trợ Cơ Sở/Y Tế. | Cập Nhật Làn Y Tế. Điều Chỉnh Sắp Xếp. |
| **Suy Thoái / Giảm Hiệu Suất (BÀI-171)** | Kích Hoạt Giao Thức Suy Thoái. | Kích Hoạt Giao Thức Chẩn Đoán. | Kiểm Tra Hỗ Trợ HLV/Đồng Nhóm. | Kích Hoạt Giao Thức Hỗ Trợ Cha Mẹ. |
| **Thay Đổi HLV** | Onboarding COO Mới. | **Sổ Tay Mới v1.0.** | Tích Hợp Phát Triển HLV. | Kế Hoạch Giao Tiếp Cha Mẹ. |
| **Thay Đổi Học Viện / Cấu Trúc** | Cập Nhật Phần Môi Trường. | Đồng Bộ Cơ Sở/Nguồn Lực. | **Sổ Tay Mới v1.0.** | Onboarding Cha Mẹ Mới. |
| **Xung Đột Cha Mẹ / Vi Phạm Ranh Giới** | Cập Nhật Phần Phúc Lợi. | Giao Thức Hỗ Trợ HLV. | Can Thiệp Cán Bộ Phúc Lợi. | **Thực Thi Hợp Đồng Làn. Trung Gian.** |
| **Kết Quả Giải Lớn (Phá Vỡ/Thất Bại)** | Tăng Tốc/Chậm Trì Tầm Nhìn. | Hiệu Chỉnh Lại Trung Chu Kỳ. | Đánh Giá Lại Nhận Diện Tài Năng. | Reset Kỳ Vọng / Tăng Cường Hỗ Trợ. |

## Bảng Điều Khiển "Nguồn Sự Thật Đơn Nhất" (SSOT)

### Bảng Điều Khiển KPI Chính (Chung Cho Tất Cả Sổ Tay)
*   **VĐ:** KPI 5 Cột Trụ, Xếp Hạng, Kết Quả Giải Đấu, Ngày Chấn Thương, HRV Cơ Sở, Ngủ, Wellness.
*   **HLV:** Tuân Thủ Kiến Trúc Buổi Tập, Tỷ Lệ Hỏi:Chỉ Dẫn, Phai Mờ Phản Hồi, Thời Gian Nói Của VĐ, Hoàn Thành Supervision, HRV HLV.
*   **Học Viện:** Giữ Chân, Đạt Cửa Giai Đoạn, Điểm Kiểm Toán HLV, NPS Cha Mẹ, Tỷ Lệ Chấn Thương, Bảo Vệ, Thu Nhận Dư.
*   **Cha Mẹ:** Tham Gia Giáo Dục, Tuân Thủ Họp Hội Đồng, Vi Phạm Hợp Đồng Làn, Tuân Thủ Ngày Thi Đấu, Sự Cố Trên Xe Hơi, Chênh Lệch Ngân Sách, Điểm Stresse.

### Ma Trận Kiểm Soát Truy Cập
| Vai Trò | KPI VĐ | KPI HLV | KPI Học Viện | KPI Cha Mẹ | Tài Chính | Y Tế |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **VĐ (CEO)** | R/W | R | R | R | R | R |
| **HLV (COO)** | R/W | R/W | R | R | R (Ngân Sách) | R (Hạn Chế) |
| **GĐKT** | R | R | R/W | R | R (Ngân Sách) | R |
| **Đại Diện Cha Mẹ** | R (Tóm Tắt) | R | R | R/W | R (Tóm Tắt) | - |
| **Cán Bộ Phúc Lợi** | R (Phúc Lợi) | R (Phúc Lợi) | R (Phúc Lợi) | R (Phúc Lợi) | - | R (Phúc Lợi) |
| **Đại Lý/Quản Lý** | R | R | R | R | R/W | - |
| **Giám Đốc Y Tế** | R (Y Tế) | R (Tải) | - | - | - | R/W |

## Gói Tài Liệu "Bộ Sổ Tay" (Sản Phẩm Đầu Ra)

### Danh Sách File (Gói Phát Hành Hàng Năm)
1.  `191_Ke_Hoach_Su_Nghiep_VD_vX.Y.md` — Tài Liệu Chiến Lược.
2.  `192_Ke_Hoach_Chuong_Trinh_HLV_vX.Y.md` — Tài Liệu Vận Hành.
3.  `193_Ke_Hoach_He_Thong_Hoc_Vien_vX.Y.md` — Tài Liệu Cơ Sở Hạ Tầng.
4.  `194_Ke_Hoach_Ho_Tro_Cha_Me_vX.Y.md` — Tài Liệu Quản Trị.
5.  `195_Chi_Muc_Bo_So_Tay_vX.Y.md` — **Tài Liệu Này (Chỉ Mục & Quản Trị).**
6.  `CHANGELOG_vX.Y.md` — Nhật Ký Thay Đổi Tích Lũy.
7.  `SSOT_Dashboard_Template.xlsx` — Mẫu Bảng Điều Khiển Chung.
8.  `Governance_Charter_vX.Y.md` — Hiến Chương Hội Đồng, Quyền Biểu Quyết, Đường Dẫn Leo Thang.
9.  `Risk_Register_vX.Y.md` — Sổ Đăng Ký Rủi Ro Thống Nhất (Chấn Thương, Suy Thoái, Xung Đột, Tài Chính, Bảo Vệ).
10. `Templates/` — Mẫu ILP, Mẫu Buổi Tập, Mẫu Họp Hội Đồng, Mẫu Ngân Sách, Mẫu CR Form.

## Vòng Lặp Cải Tiến Liên Tục ( "Kaizen" )

### Chu Kỳ Kaizen Hàng Quý
1.  **Đo Lường:** Kéo Dữ Liệu Bảng Điều Khiển SSOT.
2.  **Phân Tích:** Hội Đồng — Phân Tích Nguyên Nhân Gốc Của Các Chỉ Số Trượt.
3.  **Cải Tiến:** Phê Duyệt Yêu Cầu Thay Đổi. Cập Nhật Sổ Tay.
4.  **Kiểm Soát:** Giám Sát KPI Mới 4 Tuần. Chuẩn Hóa Hoặc Hoàn Tác.

### "Hồi Tuyển Bộ Sổ Tay" Hàng Năm
*   **Quy Trình:** Hội Đồng Offsite Toàn Thể (2-3 Giờ).
*   **Chương Trình:**
    1.  Xem Xét Năm: Thắng, Thất Bại, Bất Ngờ.
    2.  Sức Khỏe Bộ Sổ Tay: Khả Năng Sử Dụng, Tính Liên Quan, Hoàn Chỉnh.
    3.  Hiệu Quả Quản Trị: Chất Lượng Cuộc Họp, Tốc Độ Quyết Định, Giải Quyết Xung Đột.
    4.  Công Cụ: UX Bảng Điều Khiển, Ma Sát Kiểm Soát Phiên Bản, Dòng Chảy Giao Tiếp.
    5.  **Lập Kế Hoạch Phiên Bản Chính:** Phạm Vi v(X+1).0. Thay Đổi Cấu Trúc.
*   **Đầu Ra:** Hiến Chương Ký Cho Năm Sau. Cơ Sở Phiên Bản Mới.

## Hệ Thống "Cờ Đỏ" Toàn Hệ Thống
1.  **Bất Kỳ Sổ Tay Nào > 30 Ngày Quá Hạn Cập Nhật Hàng Quý.**
2.  **Bảng Điều Khiển SSOT Hiển Thị > 3 Chỉ Số Đỏ Đồng Thời.**
3.  **Cuộc Họp Hội Đồng Bị Hủy > 1 Chu Kỳ Liên Tiếp.**
4.  **Xung Đột Kiểm Soát Phiên Bản (Hai Phiên Bản Đang Dùng).**
5.  **Sự Cố Bảo Vệ Trong Bất Kỳ Lĩnh Vực Nào.**
6.  **VĐ Biểu Hiệu Mất Niềm Tin Vào Hệ Thống.**

## Ứng Dụng Thực Tế: "Hiến Chương"
Bộ Sổ Tay Là **Hiến Chương Của Doanh Nghiệp 5 Cột Trụ**. Nó Không Phải Bốn File PDF. Đó Là Một **Hệ Điều Hành Sống, Có Kiểm Soát Phiên Bản, Có Hậu Thuẫn Quản Trị**. Kế Hoạch Sự Nghiệp VĐ Xác Định Đích Đến. Kế Hoạch Chương Trình HLV Lái Xe. Kế Hoạch Hệ Thống Học Viện Xây Đường. Kế Hoạch Hỗ Trợ Cha Mẹ Cung Cấp Nhiên Liệu. Tổng Kết Bộ Sổ Tay **Lái Đưa Tàu Ngâm.** **Một Hệ Thống. Một Sự Thật. Một Phiên Bản. Một Đội Ngũ.**

## Danh Sách File Cho ART-195
Bài Tổng Kết Này (`195_Chi_Muc_Bo_So_Tay`) Phục Vụ Là **Chỉ Mục, Hiến Chương Quản Trị, Và Giao Thức Tích Hợp** Cho Bộ Sổ Tay. Nó Phải Có Mặt Trong Mọi Phiên Bản Phát Hành (`vX.Y/195_Chi_Muc_Bo_So_Tay.md`) Và Được Cập Nhật Mỗi Lúc Bump Phiên Bản.

**Hành Động Tiếp Theo:** Khởi Tạo Kho `v1.0_YYYY/` Với Tất Cả Bốn Sổ Tay + Chỉ Mục Này. Thiết Lập Bảng Điều Khiển SSOT. Lên Lịch Hội Đồng Hàng Quý Đầu Tiên. **Hệ Thống Khởi Động.**
