# ART-207: Logic App Chẩn Đoán — Động Cơ Quyết Định 5 Cột Trụ

## Tóm Tắt Điều Hành
Bài Viết Này Chi Tiết Logic, Thuật Toán, Và Cấu Trúc Dữ Liệu Cho Một "App Chẩn Đoán 5 Cột Trụ" — Một Công Cụ Hỗ Trợ Quyết Định Lâm Sàng Mã Hóa Tennis Knowledgebase Thành Các Đường Dẫn Chẩn Đoán Có Thể Thực Thi. Nó Chuyển Đổi 200 Bài Viết Kiến Thức Chuyên Gia Thành Một Hệ Thống Phần Mềm Có Cấu Trúc, Có Thể Truy Vấn, Và Có Thể Kiểm Toán Cho HLV, Y Tế, Và Vận Động Viên.

## Kiến Trúc Hệ Thống: Động Cơ Chẩn Đoán

### Triết Lý Cốt Lõi
*   **Hệ Thống Chuyên Gia, Không Phải AI Hộp Đen:** Logic Dựa Trên Quy Tắc Minh Bạch Được Dẫn Xuất Từ Các Bài 5 Cột Trụ. Mọi Khuyến Nghị Đều Truy Vết Đến Một Bài ART Cụ Thể.
*   **Chẩn Đoán Phân Biệt Trước Hết:** Không Bao Giờ Đường Đi Đơn Độc. Luôn Trình Bày Chẩn Đoán Phân Biệt Có Xếp Hạng Với Khoảng Tin Cậy.
*   **Đầu Ra Hướng Hành Động:** Chẩn Đoán → Giao Thức Khớp → Cửa Giám Sát → Ngày Xem Xét Lại.
*   **Trung Tâm Vận Động Viên:** Đầu Vào Là Báo Cáo Của VĐ + Quan Sát Của HLV + Dữ Liệu Cảm Biến. Đầu Ra Được Cá Nhân Hóa.

### Mô Hình Dữ Liệu: Vector Trạng Thái Vận Động Viên (ASV)

```typescript
interface AthleteStateVector {
  // Danh Tính & Bối Cảnh
  athleteId: string;
  timestamp: Date;
  age: number;
  biologicalAge: number;      // Độ lệch PHV
  sex: 'M' | 'F';
  handedness: 'R' | 'L';
  playingStyle: 'Baseline' | 'All-Court' | 'Serve-Volley' | 'Counterpuncher';
  currentRank: number;
  targetRank: number;
  surface: 'Clay' | 'Grass' | 'Hard' | 'Carpet';
  phase: 'Base' | 'Pre-Comp' | 'Comp' | 'Transition';
  daysSinceLastMatch: number;
  
  // Cột Trụ I: Sinh Cơ Học & Y Tế
  pillar1: {
    grfProfile: 'Vertical' | 'Horizontal' | 'Linear' | 'Mixed';
    kineticChainIntegrity: 'Intact' | 'Compromised' | 'Unknown';
    hipSeparationDeg: number;        // Đã Đo
    xFactorDeg: number;              // Đã Đo
    coreBracingScore: 1-10;          // Chủ Quan + Khách Quan
    injuryHistory: Injury[];         // Có Cấu Trúc: vị trí, loại, ngày, trạng thái RTP
    currentPain: PainMap[];          // Sơ Đồ Cơ Thể + Mức Độ 0-10
    romDeficits: ROMDeficit[];       // Khớp, Phẳng, Độ
    strengthAsymmetries: Asymmetry[]; // Chi, Chỉ Số, %
    grfAsymmetryPct: number;         // Dẫn Xuất Bàn Đạp Lực
  };
  
  // Cột Trụ II: Thần Kinh-Nhận Thức & Tinh Thần
  pillar2: {
    visualAcuity: number;            // LogMAR
    contrastSensitivity: number;     // Pelli-Robson
    depthPerception: 'Normal' | 'Reduced';
    quietEyeMs: number;              // Dẫn Xuất Eye-Tracker
    anticipationScore: number;       // Test Che Khuất %
    decisionSpeedMs: number;         // RT Lựa Chọn
    workingMemorySpan: number;       // Digit Span / n-back
    attentionalControl: 'High' | 'Moderate' | 'Low'; // Khảo Sát + Dual-Task
    csaI2rCognitive: number;         // CSAI-2R Lo Âu Nhận Thức
    csaI2rSomatic: number;           // CSAI-2R Lo Âu Thể Chất
    csaI2rConfidence: number;        // CSAI-2R Tự Tin
    pomsProfile: POMSProfile;        // Căng Thẳng, Trầm Cảm, Tức Giận, Sức Sống, Mệt Mỏi, Hỗn Loạn
    routineFidelityPct: number;      // Độ Trung Thực Nghi Thức Giữa Các Điểm
    flowStateFrequency: 'Never' | 'Rare' | 'Sometimes' | 'Often' | 'Always';
  };
  
  // Cột Trụ III: Sản Xuất Kỹ Thuật
  pillar3: {
    serve: {
      firstServePct: number;
      firstServeSpeedKph: number;
      firstServeSpinRpm: number;
      firstServePlacementAccuracy: number; // % Trong Vùng Mục Tiêu
      secondServeSpinRpm: number;
      secondServeDepthPct: number;
      tossConsistencyScore: 1-10;
      routineFidelityPct: number;
    };
    forehand: {
      grip: 'Eastern' | 'SemiWestern' | 'Western';
      contactHeightCm: number;
      contactDistanceCm: number;
      spinRpm: number;
      speedKph: number;
      depthPct: number;              // % Qua Vạch Giao Bóng
      consistencyPct: number;        // Trong Sân
      insideOutPct: number;          // Tỷ Lệ Sử Dụng
    };
    backhand: {
      type: '1HBH' | '2HBH';
      grip: string;
      contactHeightCm: number;
      spinRpm: number;
      speedKph: number;
      depthPct: number;
      consistencyPct: number;
      sliceUsagePct: number;
      sliceQuality: 1-10;
    };
    volley: {
      fhVolleyQuality: 1-10;
      bhVolleyQuality: 1-10;
      overheadQuality: 1-10;
      transitionSuccessPct: number;
    };
    return: {
      firstServeReturnInPlayPct: number;
      secondServeAttackPct: number;
      returnDepthPct: number;
      neutralizePct: number;
    };
    movement: {
      shuffleSpeedMs: number;
      crossoverSpeedMs: number;
      cod505TimeSec: number;
      codProAgilityTimeSec: number;
      recoveryStepEfficiency: 1-10;
    };
  };
  
  // Cột Trụ IV: Chiến Thuật & Hình Học
  pillar4: {
    patternLibrary: Pattern[];       // Các Mẫu Được Đặt Tên Với Tỷ Lệ Thành Công
    firstStrikeEfficiencyPct: number;
    patternUnpredictabilityIndex: number; // Chỉ Số Entropy
    courtPositionHeatmap: Heatmap;   // Thời Gian Trong Các Vùng
    tacticalDecisionAccuracy: number; // % Lựa Chọn Tối Ưu Theo Trinh Sát
    scoutingDossierQuality: 1-10;    // Độ Hoàn Chỉnh Của Chuẩn Bị Đối Thủ
    gamePlanAdherencePct: number;    // % Điểm Chơi Theo Kế Hoạch
    momentumManagementScore: 1-10;   // HLV Đánh Giá
    scoreboardPressurePerformance: {
      breakPointSavePct: number;
      breakPointConvertPct: number;
      setPointPerformance: 'Strong' | 'Average' | 'Weak';
      matchPointPerformance: 'Strong' | 'Average' | 'Weak';
    };
    environmentalAdaptability: {
      wind: 'High' | 'Moderate' | 'Low';
      sun: 'High' | 'Moderate' | 'Low';
      altitude: 'High' | 'Moderate' | 'Low';
    };
  };
  
  // Cột Trụ V: Điều Kiện & Dòng Chảy
  pillar5: {
    physical: {
      vo2maxMlKgMin: number;
      masKph: number;
      rsaTotalTimeSec: number;       // Repeated Sprint Ability
      rsaFatigueIndex: number;
      cmjHeightCm: number;
      cmjRsi: number;                // Reactive Strength Index
      sprint10mTimeSec: number;
      sprint20mTimeSec: number;
      cod505Sec: number;
      proAgilitySec: number;
      strengthBenchPress1rmKg: number;
      strengthSquat1rmKg: number;
      strengthPullUpReps: number;
      nordicsEccentricDurationSec: number;
      injuryRiskScore: number;       // Tổng Hợp 0-100
    };
    recovery: {
      hrvBaselineMs: number;
      hrvCurrentMs: number;
      hrvTrend7d: 'Rising' | 'Stable' | 'Falling';
      sleepDurationHrs: number;
      sleepEfficiencyPct: number;
      sleepConsistencyScore: 1-10;   // Độ Lệch Giờ Ngủ/Thức
      wellnessScore: 1-10;           // Khảo Sát Hàng Ngày
      muscleSoreness: 1-10;          // Hàng Ngày
      fatigueLevel: 1-10;            // Hàng Ngày
    };
    nutrition: {
      dailyEnergyAvailabilityKcalKgFfm: number;
      carbIntakeGkg: number;
      proteinIntakeGkg: number;
      hydrationStatus: 'Euhydrated' | 'Hypohydrated';
      supplementCompliance: 'Full' | 'Partial' | 'None';
    };
    mental: {
      gritScore: number;             // Grit Scale
      resilienceScore: number;       // Connor-Davidson
      confidenceLevel: number;       // 1-10
      motivationProfile: 'Intrinsic' | 'Extrinsic' | 'Amotivated';
      burnoutRisk: 'Low' | 'Moderate' | 'High'; // MBI
    };
    travel: {
      tluLast7Days: number;          // Travel Load Units
      timeZonesCrossedLast14Days: number;
      circadianAlignmentScore: 1-10;
    };
  };
}
```

## Thuật Toán Chẩn Đoán: Các Cây Quyết Định

### Thuật Toán 1: Phân Biệt Giảm Hiệu Suất (Kiểm Toán Suy Thoái ART-171)
**Đầu Vào:** ASV Với Cờ Xu Hướng Hiệu Suất (KPIs Giảm > 2 Tuần)
**Quy Trình:**
```
1. KIỂM TRA Cờ Cột Trụ V Phục Hồi:
   NẾU hrvTrend7d == 'Falling' VÀ wellnessScore < 6 VÀ fatigueLevel > 6
     → CHÍNH: Suy Thoái Thể Chất (Giao Thức Thoát Thể Chất ART-171)
     → ĐỘ TIN CẬY: CAO
   NẾU injuryRiskScore > 70 HOẶC currentPain.max > 4
     CHÍNH: Suy Thoái Thể Chất/Y Tế
     ĐỘ TIN CẬY: CAO

2. KIỂM TRA Cờ Cột Trụ II Tinh Thần:
   NẾU csaI2rCognitive > 25 HOẶC routineFidelityPct < 80 HOẶC flowStateFrequency Trong ['Never','Rare']
     → CHÍNH: Suy Thoái Tinh Thần (Giao Thức Thoát Tinh Thần ART-171)
     ĐỘ TIN CẬY: CAO

3. KIỂM TRA Cờ Cột Trụ III Kỹ Thuật:
   NẾU serve.firstServePct < baseline - 10% HOẶC forehand.consistencyPct < baseline - 15%
     → CHÍNH: Suy Thoái Kỹ Thuật (Giao Thức Thoát Kỹ Thuật ART-171)
     ĐỘ TIN CẬY: TRUNG BÌNH

4. KIỂM TRA Cờ Cột Trụ IV Chiến Thuật:
   NẾU patternUnpredictabilityIndex < baseline - 20% HOẶC gamePlanAdherencePct < 50%
     → CHÍNH: Suy Thoái Chiến Thuật (Giao Thức Thoát Chiến Thuật ART-171)
     ĐỘ TIN CẬY: TRUNG BÌNH

5. KIỂM TRA Môi Trường:
   NẾU tluLast7Days > 50 HOẶC timeZonesCrossedLast14Days > 6
     → GÓP PHẦN: Suy Thoái Môi Trường (Giao Thức Du Lịch ART-169)

ĐẦU RA: Chẩn Đoán Phân Biết Có Xếp Hạng Với % Tin Cậy + Các Giao Thức Thoát Khớp
```

### Thuật Toán 2: Phân Loại Thất Bại Dưới Áp Lực (ART-176 Sụp Đổ vs Hoảng Loạn)
**Đầu Vào:** Dữ Liệu Sự Kiện Trận Đấu + Các Chỉ Dấu Sinh Học/Nhận Thức ASV
**Quy Trình:**
```
CHO TỪNG SỰ KIỆN THẤT BÁI DƯỚI ÁP LỰC (Đối mặt BP, MP, Set Point, Tiebreak):
  THU THẬP: HR tại sự kiện, HRV trước sự kiện, báo cáo tải nhận thức tự thân, mã hóa hành vi video
  
  NẾU (HR < 85% max) VÀ (báo cáo tải nhận thức == 'Cao - Kỹ Thuật') 
     VÀ (hành vi: đóng băng, tiếp xúc muộn, vung rút gọn)
     → CHẨN ĐOÁN: SÚP ĐỔ (PFC Hoạt Động Quá Mức)
     → GIAO THỨC: ART-176 Chống Sụp Đổ (Im PFC)
     
  NẾU (HR > 90% max) VÀ (tải nhận thức == 'Trắng / Nỗi Sợ') 
     VÀ (hành vi: vội vã, hỗn loạn, thị giác hầm, thở dốc)
     → CHẨN ĐOÁN: HOẢNG LOẠN (Amygdala Hijack)
     → GIAO THỨC: ART-176 Chống Hoảng Loạn (Bình Ổn Amygdala)
     
  NẾU (HR > 90% max) VÀ (tải nhận thức == 'Cao - Kỹ Thuật') 
     → CHẨN ĐOÁN: VÒNG XOÁY SÚP ĐỔ-HOẢNG LOẠN
     → GIAO THỨC: TUẦN TỰ — Hoảng Loạn Trước (Reset Sinh Lý), Rồi Sụp Đổ (Im PFC)

ĐẦU RA: Phân Loại Từng Sự Kiện + kê Đơn Giao Thức Phiên
```

### Thuật Toán 3: Sẵn Sàng RTP Sau Chấn Thương (ART-148, ART-174)
**Đầu Vào:** ASV Y Tế/Thể Chất + Quyết Định Bác Sĩ Phẫu Thuật
**Quy Trình:**
```
RTP_STAGE = 0
NẾU surgeonClearance == TRUE VÀ painAtRest == 0 VÀ sleepNormalized == TRUE:
  RTP_STAGE = 1  // Hoàn Thành Giai Đoạn Bảo Vệ
  
NẾU romSymmetryPct > 95 VÀ strengthSymmetryPct > 90 
   VÀ forcePlateSymmetryPct > 90 VÀ yBalanceSymmetryPct > 90:
  RTP_STAGE = 2  // Sẵn Sàng Giới Thiệu Tải
  
NẾU trainingWeeksPainFreeHighIntensity >= 3 
   VÀ psychologicalReadinessScore > 80 (ACL-RSI/TSRQ)
   VÀ trustMetricDaily > 8 CHO 14 NGÀY LIÊN TIẾP:
  RTP_STAGE = 3  // Sẵn Sàng Mô Phỏng Thi Đấu
  
NẾU practiceMatchWins > 2 Ở Cường Độ Mục Tiêu 
   VÀ noPainNoCompensation 7 NGÀY LIÊN TIẾP:
  RTP_STAGE = 4  // Cho Phép Trở Lại Đầy Đủ

ĐẦU RA: Giai Đoạn RTP Hiện Tại + Các Cửa Đến Giai Đoạn Tiếp + Các Thiếu Hụt Cụ Thể
```

### Thuật Toán 4: Phân Loại Hồ Sơ "Không Huấn Luyện Được" (ART-175)
**Đầu Vào:** Nhật Ký Quan Sát Của HLV + Dữ Liệu Nhận Thức/Thể Chất/Quan Hệ ASV
**Quy Trình:**
```
SCORES = {
  cognitive: teachBackAccuracyPct,          // Mục Tiêu 100%
  autonomy: athleteInitiativesPerSession,   // Mục Tiêu > 2
  physical: movementScreenSymmetryPct,      // Mục Tiêu > 90%
  relational: parentCoachAlignmentScore,    // Mục Tiêu: Căn Chỉnh
  environmental: athleteEngagementScore     // Mục Tiêu > 8/10
}

PRIMARY_PROFILE = argmin(SCORES)  // Lĩnh Vực Điểm Thấp Nhất

NẾU PRIMARY_PROFILE == 'cognitive' VÀ teachBackAccuracyPct < 70:
  → CHẨN ĐOÁN: Không Khớp Nhận Thức (Giao Thức 1 ART-175)
  
NẾU PRIMARY_PROFILE == 'autonomy' VÀ athleteInitiativesPerSession == 0:
  → CHẨN ĐOÁN: Thiếu Hụt Tự Chủ/Niềm Tin (Giao Thức 2 ART-175)
  
NẾU PRIMARY_PROFILE == 'physical' VÀ movementScreenSymmetryPct < 80:
  → CHẨN ĐOÁN: Hạn Chế Thể Chất (Giao Thức 3 ART-175)
  
NẾU PRIMARY_PROFILE == 'relational' VÀ parentCoachAlignmentScore Trong ['Tension','Conflict']:
  → CHẨN ĐOÁN: Vỡ Tan Tam Giác (Giao Thức 4 ART-175)
  
NẾU PRIMARY_PROFILE == 'environmental' VÀ athleteEngagementScore < 5:
  → CHẨN ĐOÁN: Không Phù Hợp Môi Trường (Giao Thức 5 ART-175)

ĐẦU RA: Hồ Sơ Chính + Các Yếu Tố Góp Phần Phụ + Giao Thức Tái Cấu Trúc Khớp
```

### Thuật Toán 5: Sẵn Sàng Thay Đổi Lối Chơi (ART-172)
**Đầu Vào:** Yêu Cầu Của VĐ + ASV Kỹ Thuật/Thể Chất/Tinh Thần + Đánh Giá Của HLV
**Quy Trình:**
```
READINESS_SCORE = 0

// Tính Cần Thiết Chiến Lược (0-25 Điểm)
NẾU currentStyleCeilingEvidence == STRONG: READINESS_SCORE += 25
NẾU currentStyleCeilingEvidence == MODERATE: READINESS_SCORE += 15
KHÔNG: READINESS_SCORE += 5

// Phù Hợp Năng Lực Thể Chất (0-25 Điểm)
NẾU physicalToolsForNewStyle == EXCELLENT: READINESS_SCORE += 25
NẾU physicalToolsForNewStyle == ADEQUATE: READINESS_SCORE += 15
KHÔNG: READINESS_SCORE += 5

// Ngân Sách Thời Gian (0-25 Điểm)
NẾU protectionWindowMonths >= 12: READINESS_SCORE += 25
NẾU protectionWindowMonths >= 6: READINESS_SCORE += 15
KHÔNG: READINESS_SCORE += 5

// Sự Đồng Ý Tâm Lý (0-25 Điểm)
NẾU athleteAutonomyScore == HIGH: READINESS_SCORE += 25
NẾU athleteAutonomyScore == MODERATE: READINESS_SCORE += 15
KHÔNG: READINESS_SCORE += 5

NẾU READINESS_SCORE >= 80: GREEN_LIGHT = TRUE
NẾU READINESS_SCORE >= 60: YELLOW_LIGHT = TRUE (Có Điều Kiện)
KHÔNG: RED_LIGHT = TRUE

ĐẦU RA: Điểm Sẵn Sàng (0-100), Đèn Giao Thông, Điều Kiện Cụ Thể Nếu Vàng/Đỏ
```

### Thuật Toán 6: Chỉ Đơn Thích Ứng Cho VĐ 35+ (ART-173)
**Đầu Vào:** ASV Tuổi > 35 + Dữ Liệu Tất Cả Các Cột Trụ
**Quy Trình:**
```
PRESCRIPTION = {
  biomechanics: [
    "Rút gọn vung: Chuẩn bị sớm, finish gọn",
    "Giao bóng: Vị trí + Xoáy > Tốc độ. Giao vào người thành vũ khí",
    "Di chuyển: Trượt/Trôi > Sprint/Phanh. Giữ cuối sân",
    "Prehab 15p/ngày: Hông, Ngực, Cổ chân, Cái Kẻ"
  ],
  neurocognitive: [
    "Che khuất video 3 lần/tuần: Huấn luyện dự đoán",
    "Quiet Eye: Kéo dài cố định 200ms",
    "Cây quyết định: Giảm xuống 3 mẫu cốt lõi",
    "Khoảng tắt nhận thức: Không phân tích tennis ngoài tập"
  ],
  technical: [
    "Kiểm toán vũ khí: Chỉ giữ cú đánh >70% độ tin cậy",
    "Kiến trúc % cao: Giao bóng 65%+, Chéo sâu, Xoáy nặng",
    "Trang bị: RA < 62, Độ căng -4 đến -6 lbs, Lai Ruột/Poly"
  ],
  tactical: [
    "Kế hoạch trận: Buộc họ chơi game CỦA TÔI",
    "Giao +1 Thuận Tay chỉ đạo, Trả +1 Chéo Sâu Trung Hòa",
    "Quản lý năng lượng: Bỏ điểm lợi thế thấp, Tấn công điểm then chốt",
    "Nhắm vào điểm yếu liên tục"
  ],
  conditioning: [
    "Tỷ lệ: 1 Ngày Cao : 2 Ngày Thấp. KHÔNG ngày cao liên tiếp",
    "S&C: Nặng/Thể tích thấp (3x5@85%), Bóng Y/Plyo Thể tích thấp Ý định tối đa",
    "Hàng ngày 20p Linh hoạt + Thủy hóa màng",
    "Stack Phục Hồi: Ngủ 9-10h, Protein 2.5-3g/kg, Omega-3 3-4g, Creatine 5g, Collagen 15g+VitC",
    "Modalities ngân sách = Ưu tiên: Tương phản, Áp suất, Mềm mô, Đèn đỏ, Sauna",
    "HRV Hàng ngày. ACWR < 1.1. Cờ Đỏ = Giảm Tải Ngay Lập Tức"
  ],
  scheduling: [
    "Mặt sân: Ưu tiên mặt sân tốt nhất (Cứng/Cỏ > Đất Nện cho khớp)",
    "Đội hình: Con đường thực tế đến Tứ Kết/Bán Kết. Tránh tuần mài mòn",
    "Du lịch: Tối thiểu hóa nhảy múi giờ. Gom cụm địa lý",
    "Cửa sổ phục hồi: Tối thiểu 10 ngày giữa các chung kết (Lý tưởng 14+)",
    "Chu Kỳ Hóa Khối: Xây Dựng 6 Tuần/1 Tuần, Đỉnh 3 Tuần/2 Tuần, Duy Trì 2 Tuần/1 Tuần, Tái Tạo 1 Tuần/3 Tuần"
  ]
}

ĐẦU RA: Tài Liệu Giao Thức Bậc Thầy Cá Nhân Hóa
```

## Thông Tích Giao Diện App

### Các Module Đầu Vào
1.  **Check-In Sáng Hàng Ngày (2p):** Wellness, HRV, Ngủ, Sơ Đồ Đau, Động Lực
2.  **Đầu Vào HLV Hàng Tuần (10p):** Đánh Giá Kỹ Thuật/Chiến Thuật, Gắn Thẻ Video, Session RPE
4.  **Thử Thách Hàng Tháng (60p):** Thể Chất, Kỹ Thuật, Nhận Thức, Y Tế
5.  **Kích Hoạt Bởi Sự Kiện:** Nhập Dữ Liệu Trận Đấu (Hawk-Eye/Video), Báo Cáo Chấn Thương, Nhật Ký Du Lịch

### Các Module Đầu Ra
1.  **Bảng Điều Khiển (Thời Gian Thực):** Đèn Giao Thông KPIs, Mũi Tên Xu Hướng, Cờ Đỏ
2.  **Báo Cáo Chẩn Đoán (Theo Yêu Cầu):** Chẩn Đoán Phân Biệt, % Tin Cậy, Link Giao Thức
3.  **Trình Tạo Kế Hoạch Buổi Tập (Hàng Ngày):** Ràng Buộc, Thể Tích, Lịch Phản Hồi, Gợi Ý Tập Trung
4.  **Xem Xét Hàng Tuần/Tháng/Quý:** Phân Tích Xu Hướng, Tuân Thủ Giao Thức, Khuyến Nghị Chuyển Trục
5.  **Hệ Thống Cảnh Báo:** Thông Báo Đẩy Cho Cờ Đỏ (Giảm HRV, Tăng Đau, Tăng ACWR, Bỏ Lỡ Cửa RTP)

### Nhật Ký Kiểm Toán & Giải Thích
*   Mọi Khuyến Nghị Ghi Log: **Rule ID, Tham Chiếu ART, Giá Trị Đầu Vào, % Tin Cậy, Dấu Thời Gian**
*   HLV/VĐ Có Thể Truy Vấn: "Tại Sao Giao Thức Này?" → Hiển Thị Đường Dẫn Cây Quyết Định
*   "Kiểm Toán Giải Thích" Hàng Tháng: Mẫu Ngẫu Nhiên 10 Khuyến Nghị Được Xem Xét Độ Chính Xác Lâm Sàng

## Quản Trị Dữ Liệu & Quyền Riêng Tư
*   **VĐ Sở Hữu Dữ Liệu:** Xuất/Xoá Bất Kỳ Lúc Nào. Chia Sẻ = Opt-In Tường Minh Mỗi Người Nhận.
*   **Dữ Liệu Y Tế:** Kho Lưu Trữ Mã Hoá Riêng. Truy Cập = Đội Y Tế (HLV Chỉ Thấy Giai Đoạn RTP).
*   **Lưu Trữ:** Suốt Sự Nghiệp Hoạt Động + 7 Năm. Ẩn Danh Cho Nghiên Cứu Sau Khi Đồng Ý.
*   **Tuân Thủ:** GDPR, HIPAA, COPPA (Trẻ Em), WADA (Nhật Ký Bổ Sung/TUE).

## Lộ Trình Triển Khai
| Giai Đoạn | Phạm Vi | Thời Gian | Tiêu Chí Thành Công |
|-------|-------|----------|------------------|
| **MVP (Giai Đoạn 1)** | Thuật Toán 1-3 (Suy Thoái, Áp Lực, RTP) + Check-In Hàng Ngày + Bảng Điều Khiển | 3 Tháng | 10 VĐ Beta, >90% Đồng Thuận Chẩn Đoán Với Hội Đồng Chuyên Gia |
| **Giai Đoạn 2** | Thuật Toán 4-6 (Không HLV Được, Đổi Lối Chơi, Bậc Thầy) + Trình Tạo Kế Hoạch Buổi Tập | 3 Tháng | 50 VĐ, 5 HLV, Tuân Thủ Giao Thức > 85% |
| **Giai Đoạn 3** | Tích Hợp Thử Thách Đầy Đủ + Gắn Thẻ Video Tự Động + Phân Tích Dự Đoán | 6 Tháng | 200 VĐ, Độ Chính Xác Dự Đoán > 80% Cho Chấn Thương/Suy Thoái |
| **Giai Đoạn 4** | Đa Ngôn Ngữ (EN/VN/ES) + Chương Trình Chứng Chỉ HLV + API Tích Hợp Liên Đoàn | 6 Tháng | 1000+ Người Dùng, Áp Dụng Bởi Liên Đoàn |

## Ứng Dụng Thực Tế: "Cái Ong Nghề"
App Chẩn Đoán Là **Cái Ong Nghề Của Hệ Thống 5 Cột Trụ**. Nó Không Thay Thế Bác Sĩ (HLV/Y Tế) — Nó Khuếch Đại Thính Giác Của Họ. Nó Nghe Những Tiêu Âm (Trôi HRV, Quay Lùi Kỹ Thuật, Tải Nhận Thức) Trước Khi Chúng Trở Thành Vụ Sập. **Sử Dụng Hàng Ngày. Tin Cậy Chẩn Đoán Phân Biệt. Xác Minh Đơn Thuốc. Sự Nghiệp Của VĐ Là Bệnh Nhân.**
