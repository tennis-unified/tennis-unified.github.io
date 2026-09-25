# -*- coding: utf-8 -*-
"""VI archetype pools for articles 145-200. Toàn bộ văn xuôi tiếng Việt có dấu đầy đủ."""

VI_POOL = {}

# ----------------------------------------------------------------------------
# TRỤ CỘT IV - CHIẾN THUẬT
# ----------------------------------------------------------------------------
VI_POOL["tactics"] = {
    "intent": [
        r"""Ra quyết định chiến thuật ở trình độ thi đấu là một **bài toán quản trị xác suất**, không phải sở thích thẩm mỹ. Mỗi bóng bạn nhận đều mang một phân phối kết quả, và mỗi bóng bạn đánh sẽ dịch chuyển phân phối đó cho pha bóng kế tiếp. Vận động viên quản trị phân phối luôn thắng vận động viên chạy theo những pha bóng hào nhoáng, bởi vì trong một trận đấu kéo dài hai giờ, sự tích lũy những lợi thế phần trăm nhỏ sẽ lấn át mọi cú winner đơn lẻ. Hệ quả thực tiễn là chiến thuật phải được huấn luyện như một **kiến trúc quyết định lặp lại được**: quét thông tin, phân loại, cam kết, thực thi, hồi phục, kiểm toán.""",
        r"""Phần lớn thất bại chiến thuật không đến từ việc thiếu chất lượng cú đánh mà từ **thất bại trong việc thu nhận thông tin trước khi bóng tới**. Vận động viên đẳng cấp bắt đầu ra quyết định sớm hơn khoảng 300-500 mili giây so với người chơi trung cấp, nhờ thói quen quét tình huống trước điểm và lập hồ sơ đối thủ. Khi tiên nghiệm chính xác, thời gian phản ứng cần thiết giảm xuống và việc chọn cú đánh gần như tự động; khi thiếu tiên nghiệm, người chơi buộc phải ứng biến muộn và rủi ro cao, làm số lỗi tự đánh bại tăng vọt.""",
        r"""Đòn bẩy trên bảng điểm làm thay đổi lựa chọn cú đánh đúng ngay cả khi quả bóng hoàn toàn giống nhau. Cú phát bóng ở tỷ số 30-15 và cú phát bóng y hệt ở tỷ số 30-40 nằm ở hai ngân sách rủi ro khác nhau, vì chi phí của một lỗi là bất đối xứng. Các đối thủ hàng đầu chủ động định giá lại rủi ro tại điểm break, điểm set và thời điểm bước vào loạt tiebreak, thay vì chơi một phong cách duy nhất từ đầu đến cuối. Kỹ năng định giá lại có chủ đích này hoàn toàn huấn luyện được, và đây là con đường nhanh nhất để thắng nhiều trận sát nút hơn mà không cần thay đổi một động tác kỹ thuật nào.""",
        r"""Lớp cuối cùng là **khả năng kiểm toán**. Trực giác chiến thuật không đo lường được thì không thể cải thiện, và cũng không thể tin cậy dưới áp lực. Một bản kiểm toán sau trận có cấu trúc sẽ biến câu chuyện trận đấu hỗn loạn thành một tập nhỏ các kết quả mẫu có thể đếm được: mẫu nào tạo ra điểm, ở trạng thái tỷ số nào, gặp độ cao bóng nào, với biên an toàn bao nhiêu. Bản kiểm toán đó chính là tín hiệu phản hồi khép kín vòng lặp giữa ý định và kết quả.""",
    ],
    "sub": [
        (
            "Hình Học Sân & Ngân Sách Sai Số Góc",
            "Mỗi mục tiêu trên sân được xác định bởi ba đại lượng hình học: **góc ngang** từ điểm tiếp xúc tới mục tiêu, **chiều cao vượt lưới** khả dụng theo góc đó, và **biên chiều sâu** trước vạch cuối sân. Ba đại lượng này tạo thành một ngân sách được bảo toàn. Mở rộng góc tới một mục tiêu chéo sân nhọn sẽ đồng thời làm giảm chiều cao vượt lưới và biên chiều sâu, đó là lý do vì sao những cú đánh góc cực đại luôn có tỷ lệ lỗi cao hơn vẻ ngoài ấn tượng của chúng.",
            [
                "Góc ngang vượt 38-42 độ so với đường giữa buộc chiều cao vượt lưới phải trên 0,9 m mới giữ nguyên biên an toàn.",
                "Biên chiều sâu sụp từ khoảng 2,5 m (dọc biên) xuống còn khoảng 1,2 m (chéo sân nhọn) với cùng tốc độ vung vợt.",
                "**Mục tiêu an toàn tỷ lệ cao nhất** là phần giữa sân ở độ sâu lớn: biên tổng hợp lớn nhất, quãng đường hồi vị ngắn nhất.",
                "Chỉ nên chi ngân sách góc khi đối thủ đã bị đẩy lệch khỏi tâm sân hơn 2,5 m.",
            ],
        ),
        (
            "Kiến Trúc Mẫu Phát Bóng +1",
            "Phát bóng không phải vũ khí kết thúc điểm mà là **nửa đầu của một mẫu hai cú**. Kiến trúc phát bóng cộng một nghĩa là người phát bóng cam kết trước một cặp vị trí: một điểm phát bóng tạo ra kiểu đỡ bóng có thể dự đoán, và một cú đánh nền đầu tiên khai thác đúng kiểu đỡ bóng đó. Cặp đôi này phải được quyết định trước khi tung bóng, để bộ pháp hồi vị đã sẵn sàng định vị cơ thể cho cú thứ hai đã định.",
            [
                "Phát vào người ở ô deuce thường được đỡ trả về giữa sân: cú +1 là forehand trong-sân đánh vào khoảng trống.",
                "Phát xoáy cắt rộng ở ô ad kéo người đỡ bóng lệch khỏi tâm sân 2,2-3,0 m: cú +1 là forehand chéo sân vào vùng trống.",
                "Tỷ lệ chuyển đổi phát bóng +1 trên 62% ở cấp câu lạc bộ và trên 71% ở cấp đẳng cấp là chuẩn cho một mẫu vận hành được.",
                "Không bao giờ phát tới vị trí mà cú đỡ bóng khả năng cao nhất của nó bạn chưa từng tập ít nhất 200 lần.",
            ],
        ),
        (
            "Vị Trí Đỡ Bóng, Kiểm Soát Chiều Sâu & Bóng Trung Hòa",
            "Đỡ bóng giao có hai mục tiêu chính đáng, và nhầm lẫn giữa chúng là lỗi chiến thuật phổ biến. Mục tiêu thứ nhất là **trung hòa** (tước đi cú +1 tức thời của người phát bóng), mục tiêu thứ hai là **tấn công** (lấy đi thời gian). Trung hòa đòi hỏi chiều sâu và độ cao; tấn công đòi hỏi tiếp xúc sớm và biên độ thu ngắn. Quyết định phụ thuộc vào chất lượng phát bóng, không phụ thuộc vào tâm trạng người đỡ.",
            [
                "Đỡ phát bóng một: đứng sau vạch cuối sân 1,2-1,6 m, chặn bóng với biên độ thu gọn, nhắm chiều sâu vượt 6,5 m tính từ lưới.",
                "Đỡ phát bóng hai: bước vào trong vạch cuối sân 0,6-1,0 m và đón bóng khi bóng đang lên để nén cửa sổ hồi vị của người phát bóng.",
                "Cú đỡ bóng rơi trong vòng 4 m tính từ lưới chuyển trực tiếp thành thế thua trong vòng hai cú ở hơn 70% trường hợp.",
                "Độ cao đỡ bóng trên 1,1 m tại mặt phẳng lưới là yếu tố dự báo mạnh nhất cho một pha bóng trung hòa.",
            ],
        ),
        (
            "Nhận Diện Mẫu Dưới Ràng Buộc Thời Gian",
            "Nhận diện là một bài toán phân loại được giải dưới hạn chót cứng. Não phải ánh xạ một số ít tín hiệu động học (góc mặt vợt, xoay hông, độ cao tiếp xúc, đường vai) vào một danh sách ngắn các quỹ đạo bóng khả năng trong khoảng 200-400 mili giây kể từ lúc đối thủ tiếp xúc bóng. Huấn luyện nhận diện nghĩa là thu nhỏ tập tín hiệu đủ để kích hoạt phân loại đúng, chứ không chỉ là đánh nhiều bóng hơn.",
            [
                "Ba tín hiệu giải quyết trên 80% dự đoán hướng: mặt vợt lúc tiếp xúc, hướng đặt bàn chân trước, và đường vai không thuận.",
                "Hoạt hóa vùng chẩm-đỉnh tăng mạnh khi tín hiệu bị che, đó là lý do các bài tập che khuất tín hiệu tăng tốc nhận diện.",
                "Độ trễ nhận diện dưới 220 mili giây hỗ trợ cam kết sớm; trên 350 mili giây người chơi bị muộn về mặt cấu trúc.",
                "Chia xu hướng đối thủ thành 3-5 mẫu có tên gọi làm giảm độ trễ quyết định nhiều hơn khối lượng lặp lại thuần túy.",
            ],
        ),
        (
            "Mô Hình Đòn Bẩy Theo Trạng Thái Tỷ Số",
            "Không phải mọi điểm đều bình đẳng, và đối xử với chúng như bình đẳng là một sự đắt đỏ. Đòn bẩy là mức thay đổi xác suất thắng do điểm kế tiếp tạo ra. Phát bóng ở 30-40 trên giao của mình là điểm đòn bẩy cao vì cái giá của thất bại là mất break; phát bóng ở 40-0 là đòn bẩy thấp vì cái giá gần như bằng không. Vận động viên đẳng cấp chủ động mở rộng hoặc thu hẹp phong bì rủi ro theo đòn bẩy.",
            [
                "Ở đòn bẩy cao, thu hẹp rủi ro: nâng mục tiêu tỷ lệ phát bóng một lên 6-10 điểm phần trăm và ưu tiên cú phát có biên an toàn lớn hơn.",
                "Ở đòn bẩy thấp, mở rộng rủi ro: thử một mẫu phụ hoặc một cú phát tỷ lệ thấp mà bạn định dùng về sau trong trận.",
                "Tỷ lệ chuyển đổi điểm break tăng khi người đỡ bóng chọn trước một mẫu thay vì phản ứng lại cú phát bóng.",
                "Các điểm tiebreak từ 4-4 trở lên hành xử như game đòn bẩy cao; quy tắc thu hẹp rủi ro áp dụng tương tự.",
            ],
        ),
        (
            "Lập Hồ Sơ Đối Thủ & Bản Đồ Khai Thác",
            "Hồ sơ đối thủ là một **công cụ quyết định đã nén**, không phải một bản báo cáo trinh sát dài. Nó phải nằm gọn trên một tấm thẻ và chứa bốn mục: vị trí phát bóng ưa thích dưới áp lực, hướng di chuyển phòng thủ yếu nhất, cú đánh mắc lỗi nhiều nhất dưới độ cao bóng, và mẫu đối thủ dùng để thoát khỏi thế khó. Mọi thứ khác là nhiễu và sẽ không được nhớ lại ở tỷ số 4-4 set thứ ba.",
            [
                "Hồ sơ xây từ hơn 20 điểm quan sát dự đoán hướng đúng 65-75% số lần, so với khoảng 50% của trực giác nền.",
                "Mục hồ sơ giá trị nhất là **mẫu thoát hiểm**: nó cho biết cần phong tỏa điều gì khi đối thủ đang phòng thủ.",
                "Khai thác hướng di chuyển yếu nên được kiểm tra hai lần mỗi set trước khi tin dùng như một chiến thuật.",
                "Cập nhật hồ sơ ở mỗi lần đổi sân giúp tránh giả định cũ sau khi đối thủ điều chỉnh.",
            ],
        ),
    ],
    "step": [
        ("Quét Trước Điểm", "0-4 giây trước khi tung bóng hoặc giao bóng", "Quét vị trí, độ rộng tư thế và cách cầm vợt của đối thủ trước khi cam kết bất kỳ ý định nào. Ghi nhận tín hiệu giàu thông tin nhất và loại bỏ phần còn lại."),
        ("Khóa Ý Định", "3-1 giây trước tiếp xúc", "Tuyên bố một mục tiêu chính và một phương án dự phòng. Một điểm có hai ý định ngang nhau thực chất là không có ý định nào."),
        ("Thời Điểm Tung Bóng / Split", "Đỉnh tung bóng hoặc lúc đối thủ tiếp xúc", "Neo điểm kích hoạt di chuyển vào lúc đối thủ tiếp xúc bóng, không phải vào đường bay của bóng, để giành 80-120 mili giây quyết định cú đánh tấn công hay phòng thủ."),
        ("Định Hướng Bước Đầu", "0-250 mili giây sau tiếp xúc", "Bước đầu phải giải bài toán hình học lớn nhất trước: sâu hay ngắn, rộng hay giữa. Bước hồi vị chéo bị cấm ở giai đoạn này."),
        ("Cửa Sổ Phân Loại", "250-500 mili giây sau tiếp xúc", "Phân loại bóng thành tấn công được, trung hòa, hoặc phòng thủ. Phân loại quyết định độ dài biên độ, lực ép cầm vợt và biên mục tiêu trước khi bóng tới."),
        ("Ngưỡng Cam Kết", "500-650 mili giây sau tiếp xúc", "Khi phân loại đã xong, quyết định không được sửa lại. Sửa muộn tạo ra giảm tốc và lỗi 'nửa cú' kinh điển."),
        ("Thực Thi & Kỷ Luật Biên", "Cửa sổ tiếp xúc cộng trừ 60 mili giây", "Áp dụng biên tương ứng với phân loại: bóng tấn công được thì nhắm mục tiêu tham vọng, bóng phòng thủ thì ưu tiên chiều cao vượt lưới tối đa và chiều sâu."),
        ("Hồi Vị & Tái Lập", "0-1,2 giây sau tiếp xúc của bạn", "Hồi vị về đường phân giác các góc khả dụng của đối thủ, rồi tái lập quét trước điểm. Quãng đường hồi vị phải cân bằng, không bao giờ là chạy nước rút về vạch giữa."),
    ],
    "metric": [
        ("Điểm Thắng Phát Bóng Một", "Điểm thắng / phát bóng một vào sân", "62-68%", "72-78%"),
        ("Điểm Thắng Phát Bóng Hai", "Điểm thắng / phát bóng hai vào sân", "48-53%", "56-62%"),
        ("Chuyển Đổi Phát Bóng +1", "Điểm thắng khi cú +1 rơi vào một phần ba dự định", "58-64%", "68-74%"),
        ("Chiều Sâu Đỡ Bóng", "Khoảng cách rơi trung bình tính từ lưới (m)", "5,5-6,5 m", "6,5-7,5 m"),
        ("Chuyển Đổi Điểm Break", "Điểm break chuyển đổi / điểm break tạo được", "35-42%", "45-55%"),
        ("Lỗi Tự Đánh Bại Mỗi Set", "Số lỗi tự đánh bại được đếm mỗi set", "9-13", "4-7"),
        ("Tuân Thủ Mẫu", "Điểm thực thi đúng mẫu đã tuyên bố trước", "55-65%", "75-85%"),
        ("Thắng Khi Lên Lưới", "Điểm thắng / số lần lên lưới", "58-64%", "68-75%"),
    ],
    "error": [
        ("Đánh quá lực ở điểm đòn bẩy cao", "Phong bì rủi ro được định giá bằng cảm xúc thay vì bằng đòn bẩy", "Điểm break và điểm set bị tặng lại bằng những pha thử tỷ lệ thấp", "Định giá lại rủi ro một cách tường minh: tại điểm break, nâng tỷ lệ phát bóng một thêm 6-10 điểm và nhắm vào một phần ba giữa sân ở độ sâu lớn"),
        ("Phát bóng cùng một vị trí khi đang dẫn trong game", "Tìm kiếm sự thoải mái khi áp lực cảm nhận thấp", "Đối thủ vào nhịp một mẫu đỡ bóng và chuyển hóa nó ở điểm đòn bẩy cao kế tiếp", "Luân chuyển vị trí phát bóng theo quy tắc cố định (ví dụ không bao giờ lặp lại cùng một phần ba hai lần liên tiếp ở 30-0 hoặc 40-15)"),
        ("Đỡ phát bóng hai từ phía sau vạch cuối sân", "Sợ bị đánh xuyên qua hơn là cam kết tấn công", "Người phát bóng hoàn tất hồi vị và cú đỡ chỉ còn là pha bóng trung hòa trong trường hợp tốt nhất", "Bước vào trong vạch cuối sân 0,6-1,0 m khi đỡ phát bóng hai và đón bóng lúc bóng đang lên"),
        ("Phân loại muộn tạo ra cú đánh nửa vời", "Bóng được nhìn nhưng không được phân loại cho tới sau khi bóng nảy", "Giảm tốc lúc tiếp xúc, thu ngắn theo đà, bóng rơi giữa sân thành bóng dễ ăn", "Buộc phải phân loại sớm bằng lời ('tấn công / trung hòa / phòng thủ') ngay lúc đối thủ tiếp xúc bóng"),
        ("Đuổi theo góc chéo sân nhọn khi đối thủ chưa bị đẩy lệch", "Cú đánh được chọn vì thẩm mỹ thay vì vì hình học", "Tỷ lệ lỗi tăng gấp đôi trong khi đối thủ không hề bị di chuyển", "Chỉ chi ngân sách góc khi đối thủ đã lệch khỏi tâm sân hơn 2,5 m"),
        ("Hồi vị về vạch giữa thay vì về đường phân giác", "Thói quen đã ghi nhớ thay vì tính toán hình học", "Phần sân trống bị lộ và bóng kế tiếp buộc phải chạy nước rút tối đa", "Hồi vị về đường phân giác các góc khả dụng của đối thủ, có trọng số theo phương án tốt nhất của họ"),
        ("Bỏ qua mẫu thoát hiểm của đối thủ", "Thẻ hồ sơ quá dài để nhớ lại dưới áp lực", "Đối thủ liên tục thoát khỏi thế phòng thủ", "Chỉ giữ bốn mục hồ sơ, và tập trước mẫu phong tỏa đường thoát hiểm trước trận"),
        ("Từ bỏ mẫu sau một lần thất bại", "Thiên kiến kết quả: đánh giá quyết định bằng một kết quả đơn lẻ", "Các mẫu khả thi bị loại bỏ vì nhiễu thống kê", "Đánh giá một mẫu qua tối thiểu năm lần thực thi trước khi đổi kế hoạch"),
    ],
    "drill": [
        ("Kiến Trúc Phát Bóng +1", "Phát bóng, rồi lập tức đánh cú +1 đã tuyên bố vào vùng mục tiêu 2 m", "4 x 10 lần phát", "Tuyên bố mục tiêu trước khi tung bóng, không phải sau khi bóng được đỡ", "60 giây giữa các hiệp"),
        ("Thang Chiều Sâu Đỡ Bóng", "Đỡ phát bóng một và hai, chỉ tính điểm những cú rơi xa hơn 6 m", "3 x 12 cú đỡ", "Chiều sâu trước, tốc độ sau", "45 giây"),
        ("Nhận Diện Có Che Khuất", "Đồng đội che mặt vợt tới 200 mili giây trước tiếp xúc; gọi hướng thành tiếng", "4 x 15 bóng", "Gọi sớm, chấp nhận sai, rồi sửa", "30 giây"),
        ("Mô Phỏng Đòn Bẩy", "Chơi tiebreak bắt đầu từ 4-4 với luật tính điểm thường nhưng quy tắc rủi ro thu hẹp", "5 loạt tiebreak", "Từ 4-4 trở đi, tỷ lệ phát bóng một trên hết tham vọng", "2 phút giữa các loạt"),
        ("Set Tuân Thủ Mẫu", "Chơi set 4 game với một mẫu cố định mỗi game, có đồng đội ghi nhận", "4 game", "Thực thi kế hoạch; đừng chấm điểm các pha bóng", "90 giây"),
        ("Tấn Công Sau Khi Đẩy Lệch", "Tung bóng, đồng đội hồi vị về giữa, bạn phải đẩy họ lệch hơn 2,5 m trước khi tấn công", "3 x 8 điểm", "Đẩy lệch trước, tấn công sau", "60 giây"),
    ],
    "video": [
        "Quan sát bộ pháp hồi vị của người phát bóng ngay sau tiếp xúc: những tay giao bóng đẳng cấp đã thăng bằng sẵn cho cú +1 trước khi bóng đỡ vượt qua lưới.",
        "Chú ý độ cao tư thế của người đỡ bóng khi đỡ phát bóng hai - tư thế nghiêng tới trước, bước vào trong là dấu hiệu thị giác của ý định đỡ bóng tấn công.",
        "Ghi nhận góc đường vai lúc đối thủ tiếp xúc; tín hiệu đơn lẻ này dự báo hướng đáng tin hơn cả việc theo dõi mặt vợt.",
        "Theo dõi vị trí hồi vị sau mỗi cú: những tay mạnh nhất hồi vị về đường phân giác động, không phải về vạch giữa sơn trên sân.",
        "Nghiên cứu mẫu giảm tốc: theo đà bị thu ngắn trên một bóng dễ là dấu hiệu thị giác của việc phân loại muộn.",
        "So sánh ngôn ngữ cơ thể giữa các trạng thái tỷ số từ 4-4 trở lên - đối thủ đẳng cấp giữ nguyên quy trình trước điểm ở đòn bẩy cao.",
    ],
    "rubric": [
        ("Nhận Thức Hình Học Sân", "Chọn mục tiêu theo thói quen; chỉ đánh vào giữa sân", "Nhận ra phần sân trống sau khi bóng đã được đánh đi", "Chọn trước mục tiêu góc dựa trên độ lệch vị trí của đối thủ", "Thao túng ngân sách sai số có chủ đích, chỉ chi góc khi độ lệch vượt 2,5 m"),
        ("Tuân Thủ Mẫu", "Không có mẫu tuyên bố; chơi phản ứng từng điểm", "Tuyên bố mẫu nhưng từ bỏ sau một lỗi", "Thực thi mẫu đã tuyên bố trong hầu hết pha bóng trung hòa", "Thực thi và định giá lại mẫu theo đòn bẩy trạng thái tỷ số"),
        ("Tốc Độ Nhận Diện", "Phản ứng với bóng sau khi bóng nảy", "Phân loại kiểu bóng sau khi bóng nảy", "Phân loại trước khi bóng nảy bằng hai tín hiệu", "Phân loại trước khi bóng nảy bằng tín hiệu thứ ba và cam kết không sửa"),
        ("Tích Hợp Phát Bóng +1", "Coi phát bóng là cú đánh độc lập", "Bộ pháp hồi vị đôi khi phù hợp với cú +1 dự định", "Hồi vị luôn nạp sẵn cú +1 dự định", "Cú +1 được chọn để khai thác cú đỡ khả năng cao nhất của đối thủ, tuyên bố trước khi tung bóng"),
        ("Kỷ Luật Đòn Bẩy", "Một mức rủi ro cho mọi điểm", "Biết điểm break nhưng không điều chỉnh mục tiêu", "Thu hẹp rủi ro ở đòn bẩy cao và mở rộng ở đòn bẩy thấp", "Định lượng điều chỉnh rủi ro và xem lại sau trận"),
        ("Thực Hành Kiểm Toán Trận", "Không xem lại sau trận", "Nhớ lại một ấn tượng chung", "Đếm kết quả mẫu sau trận", "Đếm kết quả mẫu theo trạng thái tỷ số và cập nhật hồ sơ đối thủ trước trận kế tiếp"),
    ],
    "dosage": [
        "Bài tập mẫu chiến thuật thuộc **phần đầu buổi tập khi còn sung sức**: chất lượng quyết định sụt giảm đo được sau 70-80 phút đánh bóng cường độ cao, sớm hơn nhiều so với cảm nhận mệt mỏi thể chất.",
        "Hai tới ba khối chiến thuật mỗi tuần là đủ để cố kết mẫu; thêm khối lượng mà không có phản hồi tính điểm sẽ không tạo ra cải thiện đo được.",
        "Mỗi khối chiến thuật phải có ít nhất một **điều kiện tính điểm** (tiebreak, set 4 game, hoặc điểm mục tiêu); tập mẫu không tính điểm tạo ra thực thi mà không có cam kết.",
        "Tổng tải quyết định mỗi tuần nên được giới hạn để không buổi nào vượt khoảng 120 quyết định đòn bẩy cao; vượt ngưỡng đó, mức tuân thủ giảm nhanh hơn mức tăng thể lực.",
    ],
    "decision": [
        "Nếu chiều sâu đỡ bóng trung bình của đối thủ dưới 5,5 m, hãy phát bóng lên lưới hoặc tấn công cú +1 ngay; không có pha bóng trung hòa nào để giành.",
        "Nếu mức tuân thủ mẫu của bạn dưới 55% qua hai set, hãy đơn giản hóa về một mẫu duy nhất cho tới khi mức tuân thủ phục hồi, rồi mở rộng lại.",
        "Nếu lỗi tự đánh bại vượt 12 lỗi mỗi set mà không có winner bù lại, hãy thu hẹp phong bì rủi ro trước khi thay đổi kỹ thuật.",
        "Nếu đối thủ liên tục thoát khỏi thế phòng thủ, mẫu thoát hiểm - chứ không phải cú đánh phòng thủ - là mục tiêu của điều chỉnh kế tiếp.",
    ],
    "progression": [
        "Tuần 1-2: một mẫu tuyên bố mỗi game, có đồng đội ghi nhận, không áp lực tỷ số.",
        "Tuần 3-4: hai mẫu mỗi game, tiebreak tính điểm, và một hồ sơ đối thủ viết tay được cập nhật mỗi set.",
        "Tuần 5-8: mô hình hóa đòn bẩy đầy đủ với rủi ro thu hẹp tại điểm break, kèm kiểm toán sau trận về mức tuân thủ mẫu theo trạng thái tỷ số.",
    ],
}

# ----------------------------------------------------------------------------
# TRỤ CỘT V - THỂ LỰC
# ----------------------------------------------------------------------------
VI_POOL["conditioning"] = {
    "intent": [
        r"""Chuẩn bị thể chất cho tennis **không phải** là thể lực tổng quát cầm vợt trên tay. Tennis là môn thể thao gián đoạn, đa hướng, giảm tốc mạnh, trong đó những phẩm chất sinh lý quyết định là khả năng chạy nước rút lặp lại, năng lực hãm lệch tâm, sức bền công suất xoay và tốc độ phục hồi tự chủ. Huấn luyện bỏ qua dấu hiệu tải thực tế của môn sẽ tạo ra vận động viên kiểm tra rất tốt nhưng sụp đổ ở set thứ ba, vì họ đã huấn luyện những phẩm chất trận đấu không đòi hỏi và bỏ quên những phẩm chất trận đấu thực sự cần.""",
        r"""Thích nghi là một **quan hệ liều - đáp ứng có số hạng phục hồi ở mẫu số**. Cùng một buổi tập có thể là đồng hóa hoặc phá hủy tùy vào vị trí của nó so với kích thích trước đó. Vì vậy thứ tự các ngày tập nặng, bối cảnh giấc ngủ và dinh dưỡng giữa chúng, và việc theo dõi khách quan các dấu hiệu phục hồi quan trọng ngang với nội dung buổi tập. Huấn luyện thể lực mà không quản lý phục hồi chỉ đơn thuần là tích lũy mệt mỏi kèm theo một cuốn nhật ký tập.""",
        r"""Phẩm chất bị bỏ quên nhiều nhất ở cấp thi đấu là **năng lực lệch tâm và đẳng trường** - khả năng hấp thụ lực và giữ vững tư thế. Các điểm bóng tennis được quyết định trong 80-150 mili giây sau khi đổi hướng, nơi yếu tố giới hạn không phải sức mạnh đồng tâm mà là khả năng hãm, ổn định và tái tăng tốc mà không rò rỉ năng lượng qua thân người và hông. Vận động viên chỉ tập công suất đồng tâm sẽ cải thiện đầu ra ở trường hợp tốt nhất trong khi vùng tư thế xấu nhất - vùng quyết định trận đấu - vẫn không được cải thiện.""",
        r"""Cuối cùng, mọi quyết định thể lực phải được lọc qua **hồ sơ đáp ứng cá nhân**. Tuổi thời gian, tuổi tập luyện, kiến trúc giấc ngủ, pha chu kỳ kinh nguyệt khi liên quan, tiền sử chấn thương và nền tự chủ thần kinh đều dịch chuyển liều phù hợp với biên độ lớn. Các phác đồ công bố cho nhóm vận động viên đẳng cấp là giả thuyết cần kiểm chứng trên từng cá nhân, không phải đơn thuốc áp dụng nguyên bản.""",
    ],
    "sub": [
        (
            "Nhu Cầu Hệ Năng Lượng Của Trận Đấu",
            "Một trận tennis thi đấu là **dạng lai yếm khí alactic - ưa khí**: phần lớn các điểm kéo dài dưới 10 giây và được ngăn cách bởi 20-25 giây phục hồi, nên hệ phosphagen cung cấp phần công việc quyết định trong khi hệ ưa khí chi phối tốc độ tái tổng hợp hệ đó giữa các điểm và giữa các game. Do đó ưu tiên huấn luyện đi theo khoảng phục hồi, chứ không theo độ dài điểm.",
            [
                "Độ dài điểm trung bình là 4-8 giây trên sân đất nện và 3-6 giây trên sân cứng; tỷ lệ làm việc - nghỉ tập trung quanh 1:3 đến 1:5.",
                "Thời lượng trận 90-180 phút với 45-60% thời gian ở trạng thái hồi phục tích cực ngụ ý đóng góp ưa khí cao vào tổng chuyển hóa năng lượng.",
                "Tái tổng hợp phosphocreatine có một thành phần nhanh và một thành phần chậm, với khoảng 85-95% được phục hồi sau 60-90 giây nghỉ hoàn toàn.",
                "Huấn luyện khoảng phục hồi (20-25 giây) có tính chuyển giao cao hơn huấn luyện độ dài điểm tối đa.",
            ],
        ),
        (
            "Thích Nghi Thần Kinh Cơ & Gân",
            "Gân và mô liên kết thích nghi **chậm hơn cơ**, và đây là lý do cấu trúc khiến việc tăng tải nhanh tạo ra bệnh lý gân trước khi tạo ra hiệu suất. Chuyển hóa collagen cần tải cơ học kèm thời gian phục hồi thỏa đáng, và đáp ứng tốt nhất với tải vừa phải áp dụng thường xuyên hơn là tải tối đa áp dụng thưa thớt.",
            [
                "Tổng hợp collagen đạt đỉnh khoảng 24-36 giờ sau tải và còn tăng tới 72 giờ, điều này đặt khoảng cách tối thiểu cho các buổi tải va đập cao.",
                "Phác đồ đẳng trường và kháng lực chậm - nặng tạo hiệu ứng giảm đau có thể che giấu bệnh lý đang diễn ra; phải theo dõi cơn đau chứ không chỉ triệt tiêu nó.",
                "Độ cứng gân bánh chè và gân Achilles tăng đo được qua 8-12 tuần tải tiến triển; nhảy khối lượng đột ngột trên 20% mỗi tuần sẽ đảo ngược xu hướng đó.",
                "Năng lực lệch tâm dưới 1,5 lần khối lượng cơ thể ở sức bền nhón gót một chân là cờ hiệu thực tiễn cho nguy cơ chi dưới.",
            ],
        ),
        (
            "Phục Hồi Tự Chủ & Các Dấu Hiệu Theo Dõi",
            "Trạng thái tự chủ quyết định một buổi tập sẽ được hấp thụ hay bị tích lũy. Bộ theo dõi thực tiễn được giữ cố ý nhỏ: **nhịp tim nghỉ, biến thiên nhịp tim, thời lượng và chất lượng giấc ngủ, cảm nhận mức sẵn sàng, và tải theo RPE buổi tập**. Xu hướng trên cửa sổ trượt 7 ngày mang thông tin mà giá trị một ngày lẻ không có.",
            [
                "Biến thiên nhịp tim giảm trên 10-12% theo xu hướng trượt 7 ngày kèm nhịp tim nghỉ tăng 5-7 nhịp mỗi phút cho thấy căng thẳng tích lũy.",
                "RPE buổi tập nhân với thời lượng (đơn vị tùy ý) cho một chỉ số tải theo dõi được tiến triển tuần này qua tuần khác mà không cần thiết bị phòng thí nghiệm.",
                "Tỷ lệ tải cấp tính trên tải mãn tính vượt khoảng 1,5 có liên quan tới nguy cơ chấn thương cao hơn trong các môn gián đoạn.",
                "Ngủ dưới 7 giờ trong nhiều đêm liên tiếp làm giảm cả nhanh nhẹn phản ứng và độ chính xác quyết định trước khi làm giảm sức mạnh thô.",
            ],
        ),
        (
            "Chu Kỳ Hóa & Phân Bổ Tải",
            "Chu kỳ hóa là việc sắp xếp có chủ đích các căng thẳng để thích nghi tích lũy trong khi mệt mỏi được xả định kỳ. Với tennis, ràng buộc là khối lượng kỹ thuật và chiến thuật phải giữ chất lượng cao quanh năm, nên khối lượng thể lực được phân bổ quanh thi đấu thay vì chỉ trong các khối ngoài mùa giải.",
            [
                "Cấu trúc năm thực tiễn: 8-10 tuần chuẩn bị tổng quát, 6-8 tuần chuẩn bị chuyên biệt, rồi duy trì trong mùa ở mức khoảng 40-60% khối lượng đỉnh.",
                "Giảm tải 7-14 ngày trước một giải ưu tiên với mức giảm khối lượng 40-60% bảo tồn thể lực trong khi khôi phục cân bằng tự chủ.",
                "Duy trì sức mạnh chỉ cần một buổi mỗi tuần ở khối lượng vừa phải một khi nền tảng đã được thiết lập.",
                "Ngày tập nặng nên được ngăn cách bởi ít nhất một ngày định hướng phục hồi khi buổi kế tiếp đòi hỏi chất lượng quyết định.",
            ],
        ),
        (
            "Dấu Hiệu Di Chuyển, Giảm Tốc & Đổi Hướng",
            "Di chuyển tennis bị chi phối bởi **hãm ngang và hãm chéo**. Mỗi lần đổi hướng cần một cú đặt chân, một pha hấp thụ lệch tâm và một pha tái tăng tốc, và chất lượng hãm giới hạn khả năng tăng tốc tiếp theo. Huấn luyện chỉ tốc độ đường thẳng sẽ bỏ trống mẫu được dùng thường xuyên nhất.",
            [
                "Vận động viên đẳng cấp thực hiện 3-6 lần đổi hướng mỗi điểm; lực giảm tốc có thể vượt 3-4 lần khối lượng cơ thể tại bàn chân đặt.",
                "Rút ngắn bước áp chót là dấu hiệu quan sát được của hãm hiệu quả; bước cuối dài chuyển thành điểm dừng chậm và tốn năng lượng.",
                "Chuyển tiếp từ bước ngang sang chạy nước rút nên được tập với tín hiệu bên ngoài để giữ tính phản ứng thay vì di chuyển định trước.",
                "Sức mạnh dạng mở hông và xoay ngoài là những yếu tố giới hạn kiểm soát được chính của năng lực hãm.",
            ],
        ),
        (
            "Giao Thoa Huấn Luyện Đồng Thời & Thứ Tự Buổi Tập",
            "Thích nghi sức mạnh, công suất và sức bền tương tác với nhau, và sự giao thoa phần lớn là một **bài toán thứ tự buổi tập**. Đặt bài tập ưa khí cường độ cao ngay trước bài tập sức mạnh tối đa sẽ làm giảm cả chất lượng buổi sức mạnh lẫn khả năng duy trì thích nghi, trong khi thứ tự ngược lại hoặc khoảng cách đủ lớn bảo tồn cả hai.",
            [
                "Tách buổi sức mạnh tối đa và buổi sức bền cường độ cao ít nhất 6 giờ, hoặc đặt khác ngày, khi mục tiêu là bảo tồn công suất.",
                "Thực hiện các bài bùng nổ và kỹ thuật trước các bài gây mệt trong cùng một buổi.",
                "Nạp protein 0,3 gam mỗi kilôgam trong cửa sổ sau buổi tập làm giảm hiệu ứng giao thoa thực tiễn lên thích nghi sức mạnh.",
                "Huấn luyện đồng thời là chấp nhận được trong mùa giải; ràng buộc nằm ở thứ tự và phục hồi, không nằm ở việc các phương thức cùng tồn tại.",
            ],
        ),
    ],
    "step": [
        ("Đánh Giá Nền", "Trước khối tập, buổi 60-90 phút", "Thiết lập giá trị hiện tại của cá nhân trước mọi chỉ định: sàng lọc vận động, chất lượng hãm một chân, nền ưa khí và nền tự chủ."),
        ("Cổng Sẵn Sàng", "5-10 phút trước buổi tập", "Đọc các dấu hiệu sẵn sàng trong ngày và chọn một trong ba biến thể buổi tập: như kế hoạch, giảm khối lượng, hoặc thay bằng buổi phục hồi."),
        ("Khởi Động Tổng Quát", "12-18 phút tăng dần", "Nâng thân nhiệt tiến triển, di động khớp và tạo mẫu động, không giãn tĩnh trước các bài bùng nổ."),
        ("Mồi Thần Kinh", "6-8 phút", "Các bài nhảy, ném hoặc bóng y tế thời gian ngắn chất lượng cao để nâng trần đầu ra của hệ thần kinh mà không tích lũy mệt mỏi."),
        ("Kích Thích Chính", "25-40 phút", "Mục tiêu thích nghi chính của buổi tập, thực hiện khi còn sung sức, với tiêu chuẩn kỹ thuật đầy đủ và khoảng nghỉ xác định."),
        ("Bài Phụ Trợ & Dự Phòng Chấn Thương", "15-20 phút", "Bài tập nhắm vào các yếu tố giới hạn đã nhận diện của từng cá nhân: năng lực gân, kiểm soát hông và vai, sức mạnh bàn chân và cẳng chân."),
        ("Kết Thúc Thể Lực", "10-20 phút", "Bài tập gián đoạn chuyên biệt môn ở tỷ lệ làm việc - nghỉ được kiểm soát, định cỡ theo ý đồ của khối tập hiện tại."),
        ("Hạ Nhịp & Bù Nước", "10-15 phút", "Hạ nhịp phó giao cảm, bài tập thở, và bù nước kèm carbohydrate - protein ngay sau buổi tập."),
    ],
    "metric": [
        ("Nhịp Tim Nghỉ", "Đo buổi sáng khi nằm ngửa, trung bình trượt 7 ngày", "52-58 nhịp/phút", "42-48 nhịp/phút"),
        ("Biến Thiên Nhịp Tim", "rMSSD, trung bình trượt 7 ngày", "55-75 mili giây", "80-110 mili giây"),
        ("Thời Lượng Giấc Ngủ", "Tổng thời gian ngủ mỗi đêm", "7,0-8,0 giờ", "8,0-9,0 giờ"),
        ("Tải Buổi Tập", "RPE buổi tập nhân thời lượng (đơn vị tùy ý)", "250-400 đơn vị/ngày", "400-650 đơn vị/ngày"),
        ("Tỷ Lệ Cấp Tính : Mãn Tính", "Tải 7 ngày chia tải 28 ngày", "0,8-1,3", "0,9-1,2"),
        ("Mức Giảm Chạy Nước Rút Lặp Lại", "Phần trăm giảm thời gian chạy qua 6 x 30 m", "4-7%", "2-4%"),
        ("Chất Lượng Hãm Một Chân", "Điểm rút ngắn bước áp chót (thang 0-5)", "3-4", "4-5"),
        ("Thời Gian Đổi Hướng", "Bài 5-10-5 hoặc 505 chuyên biệt tennis", "2,55-2,75 giây", "2,30-2,50 giây"),
    ],
    "error": [
        ("Tập các buổi nặng vào những ngày liên tiếp", "Chương trình được dựng từ thư viện buổi tập thay vì từ mô hình tải", "Mệt mỏi tích lũy làm giảm chất lượng quyết định và tăng nguy cơ mô mềm", "Ngăn cách ngày tập nặng bằng ít nhất một ngày định hướng phục hồi; theo dõi tỷ lệ cấp tính trên mãn tính và giữ trong khoảng 0,8 đến 1,3"),
        ("Giãn tĩnh trước các bài bùng nổ", "Thói quen khởi động truyền thống còn giữ từ huấn luyện trẻ", "Giảm công suất tức thời 4-8% trong tới 60 phút", "Thay bài giãn tĩnh trước buổi bằng di động động và mồi thần kinh, chuyển giãn tĩnh sang sau buổi tập"),
        ("Bỏ qua nợ giấc ngủ khi lý giải hiệu suất kém", "Giấc ngủ bị coi là lối sống thay vì đầu vào huấn luyện", "Dấu hiệu sẵn sàng bị đọc sai thành thiếu tập, dẫn tới tăng tải thêm", "Ghi nhận giấc ngủ mỗi đêm và coi đêm dưới 7 giờ là ràng buộc lịch trình, không phải vấn đề động lực"),
        ("Tăng khối lượng hơn 20% mỗi tuần", "Hăng hái hoặc nén lịch trước giải đấu", "Gân và mô liên kết chậm hơn cơ, gây bệnh lý gân", "Giới hạn tăng khối lượng tuần ở khoảng 10-15% và giữ một tuần trong ba ở mức tải giảm"),
        ("Chỉ tập công suất đồng tâm", "Văn hóa phòng tập nhấn mạnh nâng và nhảy thay vì hãm", "Đổi hướng vẫn chậm và tốn năng lượng dù chỉ số kiểm tra tốt", "Lập trình năng lực lệch tâm và đẳng trường ít nhất hai lần mỗi tuần với mục tiêu hãm đo lường được"),
        ("Tập sức bền ngay trước sức mạnh tối đa", "Áp lực thời gian trong một buổi tập", "Cả hai thích nghi bị làm mờ và kỹ thuật buổi sức mạnh suy giảm", "Sắp bài bùng nổ và sức mạnh trước, hoặc tách hai buổi cách nhau từ 6 giờ trở lên"),
        ("Dùng giá trị biến thiên nhịp tim một ngày để đổi kế hoạch", "Dao động hằng ngày bị hiểu là tín hiệu thay vì nhiễu", "Chương trình dao động và mất cấu trúc tiến triển", "Chỉ hành động theo xu hướng trượt 7 ngày, và hành động bằng cách điều chỉnh khối lượng thay vì hủy kích thích"),
        ("Bỏ qua bù nước và dinh dưỡng sau buổi tập", "Buổi tập kết thúc khi quả bóng cuối được đánh", "Phục hồi kéo dài và buổi kế tiếp bắt đầu từ thế thiếu hụt", "Chuẩn hóa khối hạ nhịp 10-15 phút với nước, điện giải và 0,3 gam protein mỗi kilôgam"),
    ],
    "drill": [
        ("Thể Lực Gián Đoạn Trên Sân", "6 x 45 giây di chuyển chuyên biệt môn ở tỷ lệ làm việc - nghỉ 1:2", "6 hiệp x 2 loạt", "Khớp dấu hiệu di chuyển: hãm ngang và hãm chéo, không chạy đường thẳng", "90 giây giữa các loạt"),
        ("Thang Hãm Lệch Tâm", "Nhảy hạ cánh một chân và đặt chân ngang giữ vững, 5 vị trí", "4 x 6 mỗi chân", "Hạ cánh êm; hấp thụ lực, không sụp", "60 giây"),
        ("Khối Năng Lực Gân", "Tải gân bánh chè và gân Achilles chậm - nặng, 3 giây lên / 3 giây xuống", "4 x 8", "Nhịp chậm, biên độ đầy đủ, không nảy", "90 giây"),
        ("Mạch Công Suất Xoay", "Ném bóng y tế xoay, ném bên và ném xúc", "3 x 8 mỗi bên", "Hông khởi phát, thân người truyền lực, tay kết thúc", "45 giây"),
        ("Loạt Chạy Nước Rút Lặp Lại", "6 x 30 m với 25 giây phục hồi, theo dõi mức giảm", "2 loạt", "Giữ chất lượng của hiệp đầu; dừng loạt khi mức giảm vượt 7%", "3 phút giữa các loạt"),
        ("Hạ Nhịp Tự Chủ", "Thở cơ hoành 4 giây vào / 6 giây ra với chân kê cao", "8-10 phút", "Thở ra dài hơn hít vào; hướng tới nhịp tim giảm đo được", "liên tục"),
    ],
    "video": [
        "Quan sát bàn chân đặt tại mỗi lần đổi hướng: bước áp chót phải ngắn lại, và đầu gối phải đi theo hướng mũi chân mà không sụp vào trong.",
        "Theo dõi vị trí thân người khi mệt trong các game cuối - khối tâm tăng lên và gập hông giảm là những dấu hiệu thị giác sớm nhất của tải tích lũy.",
        "Ghi nhận cơ chế thở trong 20-25 giây giữa các điểm; đối thủ đẳng cấp khôi phục nhịp thở mũi, thở cơ hoành thay vì thở hổn hển.",
        "Theo dõi hai bước đầu sau bước split: người di chuyển đẳng cấp dùng bước đầu ngắn định hướng thay vì một bước dài chậm.",
        "Nghiên cứu cơ chế tiếp đất khi giao bóng và đánh trên cao - kiểm soát lệch tâm lúc tiếp đất là nơi tích lũy phần lớn tải gân chi dưới.",
        "So sánh chất lượng di chuyển trong 15 phút đầu và 15 phút cuối buổi tập; suy giảm lớn cho thấy liều buổi tập vượt năng lực phục hồi.",
    ],
    "rubric": [
        ("Kỷ Luật Quản Lý Tải", "Buổi tập chọn theo cảm giác, không có nhật ký tải", "Có ghi buổi tập nhưng không theo dõi xu hướng", "Duy trì tỷ lệ cấp tính trên mãn tính trong 0,8-1,3 và điều chỉnh mỗi tuần", "Mô hình hóa tải theo dấu hiệu sẵn sàng và lên kế hoạch giảm tải trước giải đấu"),
        ("Năng Lực Lệch Tâm & Hãm", "Không có bài lệch tâm riêng", "Thỉnh thoảng tập tiếp đất nhưng không có mục tiêu đo được", "Khối lệch tâm hai lần mỗi tuần với chất lượng một chân được theo dõi", "Tích hợp năng lực hãm vào mẫu chuyên biệt môn với tín hiệu bên ngoài và điều kiện mệt"),
        ("Theo Dõi Tự Chủ", "Không theo dõi", "Đo nhịp tim nghỉ không thường xuyên", "Đo biến thiên nhịp tim và nhịp tim nghỉ hằng ngày, xem lại trượt 7 ngày", "Dùng xu hướng trượt để chọn giữa các biến thể buổi tập đã lên kế hoạch thay vì ứng biến"),
        ("Thực Hành Giấc Ngủ & Phục Hồi", "Giấc ngủ không được quản lý", "Biết tầm quan trọng của giấc ngủ nhưng không có dữ liệu", "Ghi thời lượng ngủ mỗi đêm, đánh dấu các đêm dưới 7 giờ", "Sắp lịch giấc ngủ và dinh dưỡng như đầu vào huấn luyện với mức tuân thủ được theo dõi"),
        ("Chuẩn Bị Gân & Khớp", "Không có bài dự phòng chấn thương", "Bài phụ trợ không thường xuyên", "Khối phụ trợ cá nhân hóa nhắm vào các yếu tố giới hạn đã nhận diện", "Năng lực gân được lập trình suốt mùa với tải tiến triển và đáp ứng đau được theo dõi"),
        ("Thứ Tự Huấn Luyện Đồng Thời", "Sức bền và sức mạnh xếp thứ tự ngẫu nhiên", "Sức mạnh thường đứng trước nhưng không nhất quán", "Bài bùng nổ và sức mạnh luôn đứng trước bài gây mệt", "Các buổi tách nhau từ 6 giờ trở lên với dinh dưỡng được định thời để giảm giao thoa"),
    ],
    "dosage": [
        "Để duy trì trong mùa giải, **hai buổi sức mạnh và hai buổi thể lực mỗi tuần** bảo tồn phần lớn thích nghi; ràng buộc không nằm ở số buổi mà ở chất lượng 20 phút đầu của mỗi buổi.",
        "Bài tập gân và phụ trợ chịu được - và hưởng lợi từ - tần suất cao hơn: 3-4 lần ngắn mỗi tuần tốt hơn một buổi dài cho thích nghi mô liên kết.",
        "Thể lực gián đoạn cường độ cao không nên vượt 2-3 lần mỗi tuần trong mùa giải, mỗi lần được giới hạn để chất lượng quyết định ngày hôm sau còn nguyên vẹn.",
        "Tuần giảm tải mỗi tuần thứ ba hoặc thứ tư (giảm khối lượng 30-40%, giữ nguyên cường độ) tạo tiến triển dài hạn tốt hơn tải liên tục ở phần lớn vận động viên.",
    ],
    "decision": [
        "Nếu xu hướng biến thiên nhịp tim 7 ngày giảm hơn 10-12% kèm nhịp tim nghỉ tăng, hãy thay buổi tập đã định bằng biến thể phục hồi ưa khí và đánh giá lại sau 24 giờ.",
        "Nếu chất lượng hãm một chân dưới 3 điểm, hãy giữ nguyên tiến triển thể lực và ưu tiên năng lực lệch tâm trong hai tuần.",
        "Nếu mức giảm chạy nước rút lặp lại vượt 7%, loạt tập phải kết thúc - tiếp tục chỉ huấn luyện khả năng chịu mệt với cái giá là chất lượng tốc độ.",
        "Nếu giấc ngủ dưới 7 giờ trong ba đêm liên tiếp, hãy giảm khối lượng buổi tập 20-30% thay vì hủy, và bảo vệ giấc ngủ đêm kế tiếp.",
    ],
    "progression": [
        "Tuần 1-3: đánh giá nền, chất lượng vận động, chuẩn bị gân ở cường độ thấp, và theo dõi tự chủ nhất quán.",
        "Tuần 4-8: tăng tiến sức mạnh và tải lệch tâm với thể lực gián đoạn chuyên biệt môn ở tỷ lệ được kiểm soát.",
        "Tuần 9-12: duy trì pha thi đấu với giảm tải được lên kế hoạch trước, giảm tải đỉnh, và quyết định tải dựa trên xu hướng sẵn sàng trượt.",
    ],
}
