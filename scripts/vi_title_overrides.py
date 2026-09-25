# -*- coding: utf-8 -*-
"""Vietnamese title overrides.

A number of catalogue entries carry an English title in the VI column. Any VI page
that renders those titles (own H1, breadcrumb, <title>, or a cross-reference bullet)
would leak English prose, so they are mapped to Vietnamese here.
"""

VI_TITLE_OVERRIDE = {
    34: "Truyền Động Học Từ Lực Đùi Tới Gia Tốc Khung Chậu",
    35: "Tạo Vector Mô Men Xoắn Ở Tư Thế Mở So Với Tư Thế Đóng",
    36: "Tận Dụng Gia Tốc Trọng Trường Trong Tung Bóng Thả Rơi",
    37: "Khóa Dây Chằng Thụ Động So Với Căng Cơ Chủ Động",
    38: "Điều Chỉnh Quán Tính Xoay Trong Khi Theo Dõi Giữa Động Tác Vung",
    39: "Căn Chỉnh Pha Công Suất Đỉnh Của Chuỗi Động Lực Học",
    40: "Kiểm Toán Hiệu Suất Cơ Sinh Học Cho Tuổi Thọ Cú Đánh",
    41: "Mắt Tĩnh (QE): Cố Định Neo Thị Giác Trước Khi Tiếp Xúc",
    42: "Phản Xạ Tiền Đình - Thị Giác (VOR) Và Ổn Định Đầu",
    43: "Vòng Phản Hồi Cảm Nhận Bản Thể Trong Theo Dõi Tốc Độ Cao",
    51: "Myelin Hóa Thần Kinh Qua Lặp Lại Chính Xác Mật Độ Cao",
    53: "Giảm Tải Nhận Thức Qua Các Suy Luận Chiến Thuật Tự Động",
    57: "Biến Thiên Nhịp Tim (HRV) Và Điều Hòa Trạng Thái Thần Kinh Tự Chủ",
    60: "Yếu Tố Dinh Dưỡng Thần Kinh Nguồn Gốc Não (BDNF) Và Tiếp Thu Kỹ Năng Vận Động",
    69: "Tối Ưu Hóa Xung Thần Kinh Trong Pha Tăng Tốc Giao Bóng",
    70: "Đồng Bộ Hai Bán Cầu Não Trong Các Vận Động Hai Bên",
    96: "Cú Slice Trái Tay: Nén Lồng Ngực Và Khép Xương Bả Vai",
    119: "Cơ Học Vô Lê Phản Ứng Dưới 0,12 Giây Ở Cự Ly Gần",
    131: "Bản Đồ Nhiệt Vùng Mục Tiêu: Phân Tích Sai Số Không Gian",
    134: "Meta Vị Trí Đỡ Bóng: Đường Cuối Sân Sâu So Với Tấn Công Trong Sân",
    163: "Tối Ưu Tỷ Lệ Làm Việc Trên Nghỉ Chuyển Hóa (1:3 So Với 1:5)",
    171: "Sức Mạnh Hãm Lệch Tâm Cho Bộ Pháp Đa Hướng",
    179: "Độ Cứng Cấu Trúc Bàn Chân Và Sức Khỏe Cân Gan Chân Trên Sân Cứng",
    180: "Huấn Luyện Bùng Nổ Va Đập Cho Phản Lực Mặt Sân Bùng Nổ",
    181: "Phòng Ngừa Viêm Gân Bánh Chè Trong Tăng Tốc Và Hãm Tốc Cao",
}

# Original English strings as they appear in catalogue-driven landing pages
EN_TITLE_IN_VI = {
    34: "Kinetic Transfer from Quad Drive to Pelvic Acceleration",
    35: "Torque Vector Generation in Open vs. Closed Stances",
    36: "Gravitational Acceleration Utilization in Drop-Feeds",
    37: "Passive Ligamentous Locking vs. Active Muscle Tension",
    38: "Rotational Inertia Adjustment during Mid-Swing Tracking",
    39: "Kinetic Chain Peak Power Phase Alignment",
    40: "Biomechanical Efficiency Audits for Stroke Longevity",
    41: "Quiet Eye (QE): Fixing Visual Anchors Before Impact",
    42: "Vestibular-Ocular Reflex (VOR) and Head Stabilization",
    43: "Proprioceptive Feedback Loops in High-Velocity Tracking",
    51: "Neural Myelination through High-Density Precision Repetitions",
    53: "Cognitive Load Reduction through Automated Tactical Heuristics",
    57: "Heart Rate Variability (HRV) and Autonomic Nervous State Regulation",
    60: "Brain-Derived Neurotrophic Factor (BDNF) and Motor Skill Acquisition",
    69: "Neural Drive Optimization during Serve Acceleration",
    70: "Inter-Hemispheric Brain Synchronization in Bilateral Movements",
    96: "Backhand Slice Drive: Chest Compression and Scapular Retraction",
    119: "Sub-0.12s Reaction Volley Mechanics at Close Range",
    131: "Target Zone Heatmaps: $P\\_{error}(x,y)$ Spatial Analytics",
    134: "Return Position Meta: Deep Baseline vs. Inside-the-Baseline Aggression",
    163: "Metabolic Work-to-Rest Ratio Optimization (1:3 vs. 1:5)",
    171: "Eccentric Deceleration Strength for Multi-Directional Footwork",
    179: "Foot Structure Rigidity & Plantar Fascia Health in Hard-Court Play",
    180: "Plyometric Shock Training for Explosive Ground Force Reaction",
    181: "Patellar Tendonitis Prevention in High Acceleration/Braking",
}
