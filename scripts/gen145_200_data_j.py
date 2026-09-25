# -*- coding: utf-8 -*-
"""Per-article knowledge data, articles 198-200."""

DATA = {
    "198": {
        "topic_en": "lower extremity triple-extension power diagnostics",
        "topic_vi": "chẩn đoán sức mạnh duỗi ba khớp chi dưới",
        "mech_en": "Triple extension - hip, knee, and ankle extending together - is the **terminal power event** of the serve, the overhead, and the first step out of a split. Diagnosing it requires separating the three joints, because a deficiency in one joint produces a characteristic compensation that cannot be corrected by training the other two.",
        "mech_vi": "Duỗi ba khớp - hông, gối và cổ chân cùng duỗi - là **sự kiện công suất cuối cùng** của động tác giao bóng, động tác trên cao, và bước đầu tiên sau bước tách. Chẩn đoán nó đòi hỏi tách riêng ba khớp, vì sự thiếu hụt ở một khớp tạo ra kiểu bù trừ đặc trưng không thể sửa bằng cách huấn luyện hai khớp còn lại.",
        "vars": [
            ["Countermovement Jump Height", "Độ cao nhảy có bước đà", "45-60 cm"],
            ["Ankle Plantarflexion Power", "Công suất gập mu cổ chân", "over 25 W/kg"],
            ["Triple Extension Sequencing Time", "Thời gian trình tự duỗi ba khớp", "under 0.35 s"],
        ],
        "subs": [
            ["Joint-by-Joint Contribution and Sequencing", "Đóng Góp Và Trình Tự Theo Từng Khớp",
             "Efficient triple extension sequences proximal to distal: hips extend first, then knees, then ankles, with the ankle contributing the final 20-30% of vertical velocity. Reversing that order - an early ankle push - is a common fault that reduces jump height by 8-15% and transfers poorly to the serve.",
             "Duỗi ba khớp hiệu quả diễn ra theo trình tự từ gốc tới ngọn: hông duỗi trước, rồi gối, rồi cổ chân, với cổ chân đóng góp 20-30% cuối cùng của vận tốc thẳng đứng. Đảo ngược trình tự đó - đẩy cổ chân sớm - là một lỗi phổ biến làm giảm độ cao nhảy 8-15% và truyền kém sang động tác giao bóng."],
            ["Diagnostic Battery", "Bộ Bài Chẩn Đoán",
             "The battery includes a countermovement jump, a squat jump to isolate concentric contribution, a single-leg vertical jump, and an ankle-specific reactive test. Together these separate elastic contribution, concentric power, unilateral deficit, and ankle stiffness.",
             "Bộ bài gồm nhảy có bước đà, nhảy từ tư thế squat để tách riêng đóng góp đồng tâm, nhảy dọc một chân, và một bài phản ứng riêng cho cổ chân. Kết hợp lại, chúng tách riêng đóng góp đàn hồi, công suất đồng tâm, thiếu hụt một bên, và độ cứng cổ chân."],
        ],
        "steps": [
            ["Separate Elastic From Concentric Contribution", "Compare countermovement jump with squat jump; a small difference indicates poor elastic utilization rather than weak muscle."],
            ["Test Unilaterally as Well as Bilaterally", "A bilateral jump can mask a significant single-leg deficit; both measures are required for a diagnosis."],
            ["Tách Đóng Góp Đàn Hồi Khỏi Đồng Tâm", "So sánh nhảy có bước đà với nhảy từ tư thế squat; chênh lệch nhỏ cho thấy việc sử dụng đàn hồi kém chứ không phải cơ yếu."],
            ["Kiểm Tra Cả Một Bên Lẫn Hai Bên", "Nhảy hai bên có thể che giấu thiếu hụt một chân đáng kể; cần cả hai phép đo để chẩn đoán."],
        ],
        "errs": [
            ["Training only bilateral jumps", "Bilateral performance is assumed to represent both limbs", "A single-leg deficit persists and reappears as braking asymmetry during play", "Include single-leg vertical and lateral tests every 6-8 weeks alongside bilateral measures",
             "Chỉ tập nhảy hai bên", "Thành tích hai bên được giả định đại diện cho cả hai chi", "Thiếu hụt một chân vẫn tồn tại và tái xuất hiện dưới dạng bất đối xứng khi hãm trong thi đấu", "Đưa bài kiểm tra dọc và ngang một chân vào mỗi 6-8 tuần song song với các phép đo hai bên"],
            ["Ignoring sequencing when power is low", "Only total output is measured", "Training targets the wrong joint and power does not improve", "Record sequencing order and timing; correct proximal-to-distal order before adding load",
             "Bỏ qua trình tự khi công suất thấp", "Chỉ tổng đầu ra được đo", "Huấn luyện nhắm sai khớp và công suất không cải thiện", "Ghi lại thứ tự và thời gian trình tự; sửa trình tự từ gốc tới ngọn trước khi thêm tải"],
        ],
        "drills": [
            ["Countermovement and Squat Jump Pair", "3 attempts each, jump height recorded", "Cặp Nhảy Có Bước Đà Và Nhảy Squat", "3 lần thử mỗi bài, ghi lại độ cao nhảy"],
            ["Ankle Reactive Series", "Pogo and ankle hop series, 3 x 15 contacts", "Chuỗi Phản Ứng Cổ Chân", "Chuỗi nhảy pogo và nhảy cổ chân, 3 x 15 lần tiếp đất"],
        ],
    },
    "199": {
        "topic_en": "central nervous system fatigue monitoring systems",
        "topic_vi": "hệ thống theo dõi mệt mỏi hệ thần kinh trung ương",
        "mech_en": "Central fatigue differs from peripheral fatigue in that it **reduces output per unit of effort without local muscular failure**. It appears as slower reaction time, reduced force accuracy, and unstable movement timing, and it requires days rather than hours to resolve, which is why monitoring must precede programming.",
        "mech_vi": "Mệt mỏi trung ương khác mệt mỏi ngoại vi ở chỗ nó **giảm đầu ra trên mỗi đơn vị nỗ lực mà không có thất bại cơ cục bộ**. Nó xuất hiện dưới dạng thời gian phản ứng chậm hơn, độ chính xác lực giảm, và nhịp vận động không ổn định, và cần nhiều ngày thay vì nhiều giờ để giải quyết, đó là lý do việc theo dõi phải đi trước việc lập trình.",
        "vars": [
            ["Reaction Time Baseline", "Nền thời gian phản ứng", "increases above 8-12%"],
            ["Force Accuracy Variability", "Độ biến thiên chính xác lực", "over 15%"],
            ["Recovery Time Required", "Thời gian phục hồi cần thiết", "48-96 h"],
        ],
        "subs": [
            ["Distinguishing Central From Peripheral Fatigue", "Phân Biệt Mệt Mỏi Trung Ương Với Ngoại Vi",
             "Peripheral fatigue reduces maximal force and resolves within 24-48 hours with nutrition and rest. Central fatigue leaves maximal force largely intact while degrading the ability to produce submaximal force accurately, which is precisely the skill tennis demands. Measuring maximal strength alone therefore misses it entirely.",
             "Mệt mỏi ngoại vi làm giảm lực tối đa và giải quyết trong 24-48 giờ với dinh dưỡng và nghỉ ngơi. Mệt mỏi trung ương để lực tối đa gần như nguyên vẹn trong khi làm suy giảm khả năng tạo lực dưới mức tối đa một cách chính xác, đúng kỹ năng mà tennis đòi hỏi. Do đó chỉ đo sức mạnh tối đa sẽ bỏ sót hoàn toàn loại mệt mỏi này."],
            ["Monitoring Battery and Decision Rules", "Bộ Theo Dõi & Quy Tắc Quyết Định",
             "A practical battery is a simple reaction-time test, a force-matching task, and a movement-timing measure, each recorded daily. Decision rules are pre-declared: a reaction-time increase above 10% for two consecutive days triggers a technical-only session with no new skill acquisition.",
             "Một bộ thực tiễn gồm bài kiểm tra thời gian phản ứng đơn giản, một nhiệm vụ khớp lực, và một phép đo nhịp vận động, mỗi thứ được ghi hằng ngày. Các quy tắc quyết định được tuyên bố trước: mức tăng thời gian phản ứng trên 10% trong hai ngày liên tiếp sẽ kích hoạt một buổi chỉ kỹ thuật, không học kỹ năng mới."],
        ],
        "steps": [
            ["Measure Daily, Not Weekly", "Central fatigue fluctuates across days; weekly testing describes an average that never occurred."],
            ["Pre-Declare the Decision Rules", "Write the thresholds and the resulting session modifications before the block begins; improvised responses under fatigue are unreliable."],
            ["Đo Hằng Ngày, Không Đo Hằng Tuần", "Mệt mỏi trung ương dao động theo ngày; kiểm tra hằng tuần mô tả một giá trị trung bình chưa từng tồn tại."],
            ["Tuyên Bố Trước Các Quy Tắc Quyết Định", "Viết các ngưỡng và các điều chỉnh buổi tập tương ứng trước khi khối tập bắt đầu; các phản ứng ứng biến khi mệt là không đáng tin."],
        ],
        "errs": [
            ["Testing only maximal strength", "Central and peripheral fatigue are assumed to be the same phenomenon", "Central fatigue accumulates undetected and skill acquisition stalls", "Add a daily reaction-time and force-accuracy measure alongside strength testing",
             "Chỉ kiểm tra sức mạnh tối đa", "Mệt mỏi trung ương và ngoại vi được giả định là cùng một hiện tượng", "Mệt mỏi trung ương tích lũy mà không bị phát hiện và việc học kỹ năng đình trệ", "Thêm phép đo thời gian phản ứng và độ chính xác lực hằng ngày song song với kiểm tra sức mạnh"],
            ["Introducing new skills while centrally fatigued", "The session plan is fixed regardless of readiness", "New patterns are encoded inaccurately and must be relearned", "Trigger technical-only sessions with no new skill acquisition when reaction time rises above 10% for two days",
             "Đưa kỹ năng mới vào khi đang mệt mỏi trung ương", "Kế hoạch buổi tập cố định bất kể mức sẵn sàng", "Các mẫu mới được mã hóa không chính xác và phải học lại", "Kích hoạt các buổi chỉ kỹ thuật, không học kỹ năng mới, khi thời gian phản ứng tăng trên 10% trong hai ngày"],
        ],
        "drills": [
            ["Daily Reaction Test", "Simple visual reaction test, five trials, recorded each morning", "Bài Kiểm Tra Phản Ứng Hằng Ngày", "Bài kiểm tra phản ứng thị giác đơn giản, năm lần thử, ghi mỗi sáng"],
            ["Force-Matching Task", "Match 50% of maximal grip force without visual feedback, five trials", "Nhiệm Vụ Khớp Lực", "Khớp 50% lực nắm tối đa mà không có phản hồi thị giác, năm lần thử"],
        ],
    },
    "200": {
        "topic_en": "master bio-agentic performance architecture integration",
        "topic_vi": "tích hợp kiến trúc hiệu suất theo phản hồi sinh học tối thượng",
        "mech_en": "The master architecture integrates the preceding pillars into a **single decision system**: technical intent defines the target, physical capacity defines what is available, recovery state defines what is tolerable today, and the audit closes the loop. Integration is not the sum of the parts but the removal of conflicts between them.",
        "mech_vi": "Kiến trúc tối thượng tích hợp các trụ cột trước đó thành **một hệ thống quyết định duy nhất**: ý định kỹ thuật xác định mục tiêu, năng lực thể chất xác định những gì khả dụng, trạng thái phục hồi xác định những gì có thể chịu được hôm nay, và bản kiểm toán khép kín vòng lặp. Tích hợp không phải là tổng của các phần mà là việc loại bỏ các xung đột giữa chúng.",
        "vars": [
            ["Integrated Review Cadence", "Nhịp xem lại tích hợp", "7 days (micro), 90 days (macro)"],
            ["Priority Quality Count", "Số phẩm chất ưu tiên", "2-3 per macrocycle"],
            ["Decision Latency Target", "Mục tiêu độ trễ quyết định", "under 24 h for load changes"],
        ],
        "subs": [
            ["The Four Inputs of the Decision System", "Bốn Đầu Vào Của Hệ Thống Quyết Định",
             "Technical intent, physical capacity, recovery state, and audit data form the input set. Conflicts arise when a plan is written from only one input - most commonly technical intent - and the resulting sessions exceed what recovery state can absorb, which is the mechanism behind most mid-season stagnation.",
             "Ý định kỹ thuật, năng lực thể chất, trạng thái phục hồi, và dữ liệu kiểm toán tạo thành tập đầu vào. Xung đột xuất hiện khi một kế hoạch chỉ được viết từ một đầu vào - thường là ý định kỹ thuật - và các buổi tập kết quả vượt quá khả năng hấp thụ của trạng thái phục hồi, và đây là cơ chế đằng sau phần lớn tình trạng đình trệ giữa mùa."],
            ["Removing Conflicts Between Pillars", "Loại Bỏ Xung Đột Giữa Các Trụ Cột",
             "Integration is mostly subtractive. Heavy strength work placed 24 hours before a high-quality tactical session is not a scheduling inconvenience but a conflict; resolving it raises total performance more than adding any single new modality.",
             "Tích hợp chủ yếu mang tính loại bỏ. Bài tập sức mạnh nặng đặt 24 giờ trước một buổi chiến thuật chất lượng cao không phải là một bất tiện về lịch mà là một xung đột; giải quyết nó nâng hiệu suất tổng thể nhiều hơn việc thêm bất kỳ phương thức mới đơn lẻ nào."],
        ],
        "steps": [
            ["Declare the Two or Three Priority Qualities", "For each macrocycle, name two or three priority qualities and accept that everything else is maintained rather than developed."],
            ["Review Weekly and Re-Plan Quarterly", "Use a 7-day review for load adjustments and a 90-day review for structural changes; mixing the two produces constant re-planning."],
            ["Tuyên Bố Hai Hoặc Ba Phẩm Chất Ưu Tiên", "Với mỗi chu kỳ lớn, gọi tên hai hoặc ba phẩm chất ưu tiên và chấp nhận rằng mọi thứ khác được duy trì thay vì được phát triển."],
            ["Xem Lại Hằng Tuần Và Tái Lập Kế Hoạch Hằng Quý", "Dùng xem lại 7 ngày cho việc điều chỉnh tải và xem lại 90 ngày cho các thay đổi cấu trúc; trộn lẫn hai nhịp sẽ tạo ra việc tái lập kế hoạch liên tục."],
        ],
        "errs": [
            ["Building the plan from technical intent alone", "Skill goals are treated as the only legitimate input", "Session load exceeds recovery capacity and progress stalls after four to six weeks", "Require all four inputs before writing a block and check recovery state against the planned load",
             "Xây kế hoạch chỉ từ ý định kỹ thuật", "Mục tiêu kỹ năng được coi là đầu vào chính đáng duy nhất", "Tải buổi tập vượt năng lực phục hồi và tiến triển đình trệ sau bốn tới sáu tuần", "Yêu cầu cả bốn đầu vào trước khi viết một khối và đối chiếu trạng thái phục hồi với tải đã định"],
            ["Adding modalities instead of resolving conflicts", "More is assumed to be better", "Total load rises while measured performance stays flat", "Resolve scheduling conflicts first and add a modality only when a specific quality remains unaddressed",
             "Thêm phương thức thay vì giải quyết xung đột", "Nhiều hơn được giả định là tốt hơn", "Tổng tải tăng trong khi hiệu suất đo được không đổi", "Giải quyết xung đột lịch trước và chỉ thêm một phương thức khi có một phẩm chất cụ thể vẫn chưa được giải quyết"],
        ],
        "drills": [
            ["Weekly Integration Review", "One page: priorities, load, readiness trend, and one change", "Xem Lại Tích Hợp Hằng Tuần", "Một trang: các ưu tiên, tải, xu hướng sẵn sàng, và một thay đổi"],
            ["Quarterly Architecture Audit", "Re-test priority qualities and revise the 90-day plan", "Kiểm Toán Kiến Trúc Hằng Quý", "Kiểm tra lại các phẩm chất ưu tiên và sửa kế hoạch 90 ngày"],
        ],
    },
}
