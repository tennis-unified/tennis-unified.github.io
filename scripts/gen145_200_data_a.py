# -*- coding: utf-8 -*-
"""Per-article knowledge data, articles 145-150."""

DATA = {
    "145": {
        "topic_en": "attacking weak second serves",
        "topic_vi": "tấn công phát bóng hai yếu",
        "mech_en": "A weak second serve is a **structurally predictable ball**: reduced spin, reduced velocity, and a higher bounce point hand the returner a fixed 250-400 ms advantage that can be converted into a decisive first strike. The tactical problem is not aggression but **positioning arithmetic** - step in too little and the return becomes neutral, step in too much and the kick serve climbs above the strike zone and the return collapses into a defensive block.",
        "mech_vi": "Phát bóng hai yếu là một **quả bóng có thể dự đoán về mặt cấu trúc**: ít xoáy hơn, tốc độ thấp hơn, và điểm nảy cao hơn trao cho người đỡ bóng một lợi thế cố định 250-400 mili giây có thể chuyển hóa thành cú tấn công quyết định. Vấn đề chiến thuật không phải là sự hung hăng mà là **số học vị trí** - bước vào quá ít thì cú đỡ trở nên trung hòa, bước vào quá nhiều thì bóng xoáy kick vượt lên trên vùng đánh và cú đỡ sụp thành một pha chặn phòng thủ.",
        "vars": [
            ["Entry Depth Inside Baseline", "Độ sâu bước vào trong vạch cuối sân", "0.6-1.0 m"],
            ["Contact Height Above Ground", "Độ cao tiếp xúc so với mặt sân", "0.9-1.15 m"],
            ["Return Depth Beyond Net", "Chiều sâu cú đỡ tính từ lưới", "6.5-7.5 m"],
        ],
        "subs": [
            [
                "Second-Serve Kinematics and the Probability Window",
                "Động Học Phát Bóng Hai & Cửa Sổ Xác Suất",
                "A second serve must clear the net by a larger margin and land inside a shorter service box, so the server trades velocity for spin and safety. That trade produces a measurable signature: 20-30% less ball speed, 15-25% more vertical bounce, and a longer flight time of roughly 80-140 ms. The returner's entire advantage is derived from that extra flight time plus the higher contact point.",
                "Phát bóng hai buộc phải vượt lưới với biên lớn hơn và rơi trong ô giao bóng ngắn hơn, nên người phát bóng đánh đổi tốc độ lấy xoáy và an toàn. Sự đánh đổi đó tạo ra một dấu hiệu đo được: tốc độ bóng giảm 20-30%, độ nảy dọc tăng 15-25%, và thời gian bay dài hơn khoảng 80-140 mili giây. Toàn bộ lợi thế của người đỡ bóng đến từ thời gian bay thêm đó cộng với điểm tiếp xúc cao hơn.",
            ],
            [
                "Stance Geometry: Closed, Neutral, and the Aggressive Diagonal",
                "Hình Học Tư Thế: Đóng, Trung Tính & Đường Chéo Tấn Công",
                "Three stance families serve different intentions. A neutral open stance preserves lateral coverage but forces a longer backswing; a closed stance loads the back hip for a cross-court drive but exposes the down-the-line; the aggressive diagonal stance - front foot angled 30-40 degrees toward the intended target - pre-rotates the pelvis so that the forward step itself becomes the first phase of the swing.",
                "Ba nhóm tư thế phục vụ ba ý định khác nhau. Tư thế mở trung tính giữ được khả năng bao quát ngang nhưng buộc biên độ vung dài hơn; tư thế đóng nạp hông sau cho cú đánh chéo sân nhưng lộ đường dọc biên; tư thế chéo tấn công - bàn chân trước xoay 30-40 độ về phía mục tiêu dự định - xoay trước khung chậu để chính bước tiến trở thành pha đầu của động tác vung.",
            ],
        ],
        "steps": [
            ["Split on the Toss, Step In on the Contact", "As soon as the server's toss leaves the hand, split; the forward step must begin at the server's contact, not after the ball crosses the net, so that the plant foot lands while the ball is still rising."],
            ["Shadow-Swing Compression Check", "Keep the backswing under 45 cm of racket travel; the incoming ball already supplies the power, and a long backswing converts a 400 ms advantage into a late, cramped contact."],
            ["Tách Bước Khi Tung Bóng, Bước Vào Khi Tiếp Xúc", "Ngay khi bóng tung rời tay người phát, thực hiện bước tách; bước tiến phải bắt đầu lúc người phát tiếp xúc bóng, không phải sau khi bóng vượt lưới, để bàn chân trụ tiếp đất khi bóng còn đang lên."],
            ["Kiểm Tra Nén Biên Độ Vung", "Giữ biên độ vung dưới 45 cm quãng đường vợt; bóng tới đã cung cấp lực, và biên độ dài biến lợi thế 400 mili giây thành một lần tiếp xúc muộn và bị chèn."],
        ],
        "errs": [
            ["Returning second serves from behind the baseline", "Habitual position carried over from first-serve returning", "The server completes recovery and the return becomes a neutral rally at best", "Mark the entry distance on the court with tape for two weeks; step in 0.6-1.0 m on every second serve until the position becomes automatic",
             "Đỡ phát bóng hai từ phía sau vạch cuối sân", "Vị trí theo thói quen được mang từ việc đỡ phát bóng một", "Người phát bóng hoàn tất hồi vị và cú đỡ chỉ còn là pha bóng trung hòa trong trường hợp tốt nhất", "Đánh dấu khoảng cách bước vào trên sân bằng băng dính trong hai tuần; bước vào 0,6-1,0 m ở mọi phát bóng hai cho tới khi vị trí trở thành tự động"],
            ["Swinging too large on a high kick serve", "Power intention is retained while the contact point rises above the strike zone", "Contact occurs late and behind the body, producing a weak floating return", "Cap racket travel at 45 cm and aim for depth rather than pace; a 6.5 m deep return wins the point more often than a 100 km/h error",
             "Vung quá lớn trước cú kick bóng cao", "Ý định dùng lực được giữ nguyên trong khi điểm tiếp xúc vượt lên trên vùng đánh", "Tiếp xúc muộn và ra sau thân người, tạo ra cú đỡ yếu và bổng", "Giới hạn quãng đường vợt ở 45 cm và nhắm chiều sâu thay vì tốc độ; cú đỡ sâu 6,5 m thắng điểm thường xuyên hơn một lỗi ở tốc độ 100 km/h"],
        ],
        "drills": [
            ["Entry-Depth Ladder", "Mark three entry depths; score only returns that land beyond 6.5 m", "Thang Độ Sâu Bước Vào", "Đánh dấu ba mức độ sâu; chỉ tính điểm những cú đỡ rơi xa hơn 6,5 m"],
            ["Kick-Return Compression", "Partner feeds high kick serves; 45 cm backswing limit enforced by a barrier", "Nén Cú Đỡ Bóng Kick", "Đồng đội tung bóng kick cao; giới hạn biên độ 45 cm được ép bằng một vật chắn"],
        ],
    },
    "146": {
        "topic_en": "wind vector adaptation",
        "topic_vi": "thích nghi vector gió",
        "mech_en": "Wind does not simply slow or speed a ball up; it **deforms the trajectory**. A headwind increases lift relative to airspeed and shortens the ball's effective depth while a tailwind has the opposite effect, which means the same stroke produces two different landing points and two different net-clearance profiles. Adaptation requires re-solving the trajectory rather than swinging harder.",
        "mech_vi": "Gió không chỉ làm bóng chậm lại hay nhanh hơn; gió **biến dạng quỹ đạo**. Gió đối làm tăng lực nâng so với tốc độ không khí và rút ngắn chiều sâu hiệu dụng của bóng, trong khi gió xuôi gây hiệu ứng ngược lại, nghĩa là cùng một cú đánh tạo ra hai điểm rơi khác nhau và hai biên vượt lưới khác nhau. Thích nghi đòi hỏi giải lại quỹ đạo thay vì vung mạnh hơn.",
        "vars": [
            ["Wind Speed Threshold for Full Adaptation", "Ngưỡng tốc độ gió cần thích nghi đầy đủ", "18-25 km/h"],
            ["Net Clearance Adjustment (Headwind)", "Điều chỉnh chiều cao vượt lưới khi gió đối", "+0.25 to +0.45 m"],
            ["Toss Displacement Tolerance", "Dung sai lệch điểm tung bóng", "under 0.30 m"],
        ],
        "subs": [
            [
                "Aerodynamic Asymmetry: Headwind vs. Tailwind",
                "Bất Đối Xứng Khí Động: Gió Đối So Với Gió Xuôi",
                "The lift force on a spinning ball scales with the square of the relative airspeed, so a headwind raises lift and steepens the descent while a tailwind reduces lift and flattens it. Quantitatively, a 20 km/h headwind can shorten a topspin groundstroke by 0.8-1.4 m of depth, while the same wind at the back can add a similar amount and push the ball long.",
                "Lực nâng tác dụng lên bóng có xoáy tỷ lệ với bình phương tốc độ không khí tương đối, nên gió đối làm tăng lực nâng và làm dốc đường rơi, còn gió xuôi làm giảm lực nâng và làm phẳng quỹ đạo. Về định lượng, gió đối 20 km/h có thể rút ngắn một cú topspin 0,8-1,4 m chiều sâu, trong khi cùng tốc độ gió đó ở lưng có thể cộng thêm tương tự và đẩy bóng ra ngoài.",
            ],
            [
                "Toss Management in Lateral Wind",
                "Quản Lý Tung Bóng Trong Gió Ngang",
                "A lateral wind displaces the toss by 0.3-0.8 m within a single second, which destroys contact consistency before the stroke even begins. Elite servers pre-tilt the toss direction by 10-20 degrees into the wind and shorten the toss height rather than attempting to compensate with the arm, because the arm has no reliable reference frame while the ball is airborne.",
                "Gió ngang làm lệch điểm tung bóng 0,3-0,8 m trong một giây, phá hủy tính nhất quán của tiếp xúc trước cả khi cú đánh bắt đầu. Người phát bóng đẳng cấp nghiêng trước hướng tung 10-20 độ về phía ngược gió và hạ thấp độ cao tung thay vì cố bù bằng tay, bởi tay không có hệ quy chiếu đáng tin trong khi bóng đang bay.",
            ],
        ],
        "steps": [
            ["Establish the Wind Baseline Before the Warm-Up", "Throw five balls in each direction during warm-up and record the observed depth change; do not estimate wind from how it feels on the skin."],
            ["Re-Solve the Target, Not the Swing", "Adjust the aim point and net clearance first; only after the target is re-solved should swing speed be modulated."],
            ["Xác Lập Nền Gió Trước Khi Khởi Động", "Ném năm quả bóng theo mỗi hướng trong khởi động và ghi lại mức thay đổi chiều sâu quan sát được; không ước lượng gió bằng cảm giác trên da."],
            ["Giải Lại Mục Tiêu, Không Giải Lại Động Tác", "Điều chỉnh điểm nhắm và chiều cao vượt lưới trước; chỉ sau khi mục tiêu được giải lại mới nên điều chỉnh tốc độ vung."],
        ],
        "errs": [
            ["Swinging harder into a headwind", "Depth loss is misread as insufficient force", "The ball climbs and lands long, or the swing degrades into a flat push", "Increase net clearance by 0.25-0.45 m and keep swing speed constant; depth is recovered through trajectory, not effort",
             "Vung mạnh hơn khi gặp gió đối", "Việc mất chiều sâu bị hiểu sai là thiếu lực", "Bóng bay cao và rơi ra ngoài, hoặc động tác suy giảm thành cú đẩy phẳng", "Tăng chiều cao vượt lưới thêm 0,25-0,45 m và giữ nguyên tốc độ vung; chiều sâu được lấy lại qua quỹ đạo, không qua nỗ lực"],
            ["Ignoring toss displacement in crosswind", "Toss technique is unchanged regardless of conditions", "Contact point varies by 20-40 cm, destroying serve percentage and placement", "Pre-tilt the toss 10-20 degrees into the wind and lower the toss apex; verify with five measured serves before the first game",
             "Bỏ qua độ lệch tung bóng khi có gió ngang", "Kỹ thuật tung bóng không thay đổi bất kể điều kiện", "Điểm tiếp xúc dao động 20-40 cm, phá hủy tỷ lệ và vị trí phát bóng", "Nghiêng trước hướng tung 10-20 độ ngược gió và hạ đỉnh tung; kiểm chứng bằng năm cú phát đo được trước game đầu"],
        ],
        "drills": [
            ["Two-Way Depth Calibration", "Hit 10 balls each direction and log landing depth; target a 0.5 m spread", "Hiệu Chuẩn Chiều Sâu Hai Hướng", "Đánh 10 bóng mỗi hướng và ghi chiều sâu điểm rơi; mục tiêu độ tán xạ 0,5 m"],
            ["Wind Serve Ladder", "Serve to three locations in both directions; score only serves inside the target box", "Thang Phát Bóng Trong Gió", "Phát tới ba vị trí ở cả hai hướng; chỉ tính điểm những cú phát vào đúng ô mục tiêu"],
        ],
    },
    "147": {
        "topic_en": "inside-out forehand court geometry",
        "topic_vi": "hình học sân của cú forehand inside-out",
        "mech_en": "The inside-out forehand is the most efficient opening creator in modern baseline tennis because it attacks from the **ad-court side of the center line** into the opponent's backhand corner while your own recovery path is the shortest available. The stroke trades 8-12 degrees of available angle for a 1.5-2.0 m reduction in recovery distance, which is why it produces more open-court opportunities than a wider cross-court ball.",
        "mech_vi": "Cú forehand inside-out là công cụ tạo khoảng trống hiệu quả nhất trong tennis đường dài hiện đại vì nó tấn công từ **phía ô ad của đường giữa** vào góc trái tay đối thủ trong khi đường hồi vị của chính bạn là ngắn nhất trong các lựa chọn. Cú đánh đánh đổi 8-12 độ góc khả dụng để lấy mức giảm 1,5-2,0 m quãng đường hồi vị, đó là lý do nó tạo ra nhiều cơ hội sân trống hơn một cú chéo sân rộng hơn.",
        "vars": [
            ["Contact Point Lateral Offset", "Độ lệch ngang của điểm tiếp xúc", "0.4-0.8 m right of center"],
            ["Recovery Distance Saved", "Quãng đường hồi vị tiết kiệm được", "1.5-2.0 m"],
            ["Crosscourt Opening Angle Created", "Góc mở chéo sân tạo được", "26-34 degrees"],
        ],
        "subs": [
            [
                "Geometric Construction of the Inside-Out Pattern",
                "Cấu Trúc Hình Học Của Mẫu Inside-Out",
                "The inside-out forehand is defined by three coordinates: the contact point (0.4-0.8 m right of the center line), the target (the opponent's backhand corner, 1.0-1.5 m inside the singles sideline), and the recovery point (the bisector of the opponent's remaining angles). The pattern's value comes from the asymmetry between the ball's travel distance and the player's recovery distance.",
                "Cú forehand inside-out được xác định bởi ba tọa độ: điểm tiếp xúc (0,4-0,8 m về phía phải đường giữa), mục tiêu (góc trái tay đối thủ, cách vạch biên đơn 1,0-1,5 m), và điểm hồi vị (đường phân giác các góc còn lại của đối thủ). Giá trị của mẫu đến từ sự bất đối xứng giữa quãng đường bóng bay và quãng đường người chơi hồi vị.",
            ],
            [
                "Hip Pre-Rotation and the Open-Stance Load",
                "Xoay Trước Hông & Nạp Lực Tư Thế Mở",
                "Because the ball arrives on the forehand side but must travel to the opposite corner, the pelvis must be pre-rotated 15-25 degrees further than in a standard cross-court forehand. This pre-rotation is what allows the open stance to produce a down-the-line-of-the-opponent trajectory without a compensating arm manipulation, which would otherwise cost 10-15% of racket-head speed.",
                "Vì bóng tới ở phía forehand nhưng phải bay tới góc đối diện, khung chậu phải được xoay trước thêm 15-25 độ so với cú forehand chéo sân tiêu chuẩn. Việc xoay trước này cho phép tư thế mở tạo ra quỹ đạo hướng vào góc đối thủ mà không cần điều khiển bù bằng tay, điều lẽ ra sẽ làm mất 10-15% tốc độ đầu vợt.",
            ],
        ],
        "steps": [
            ["Recognize the Short Ball Early", "Begin the pattern only against balls landing inside 5.5 m of the net; from deeper balls the recovery asymmetry disappears and the pattern becomes a neutral exchange."],
            ["Commit the Pelvis Before the Plant", "Pre-rotate the hips during the last two steps of the approach; attempting to rotate after the plant reduces racket-head speed by 10-15%."],
            ["Nhận Diện Bóng Ngắn Sớm", "Chỉ bắt đầu mẫu khi bóng rơi trong vòng 5,5 m tính từ lưới; với bóng sâu hơn, bất đối xứng hồi vị biến mất và mẫu trở thành pha bóng trung hòa."],
            ["Xoay Trước Khung Chậu Trước Khi Đặt Chân", "Xoay trước hông trong hai bước cuối của pha tiếp cận; cố xoay sau khi đặt chân sẽ giảm 10-15% tốc độ đầu vợt."],
        ],
        "errs": [
            ["Running around the ball too late", "The decision to run around is made after the ball has already passed the center line", "The contact point drifts behind the body and the shot loses its cross-court penetration", "Decide inside-out at the opponent's contact, not at your own split step; if the decision is late, play the natural cross-court instead",
             "Chạy vòng qua bóng quá muộn", "Quyết định chạy vòng được đưa ra sau khi bóng đã vượt qua đường giữa", "Điểm tiếp xúc trôi ra sau thân người và cú đánh mất độ xuyên chéo sân", "Quyết định inside-out ngay lúc đối thủ tiếp xúc bóng, không phải ở bước tách của bạn; nếu quyết định muộn, hãy đánh chéo sân tự nhiên"],
            ["Recovering to the center line after the inside-out", "A memorized recovery habit rather than a geometric calculation", "The open court is exposed to a single cross-court pass", "Recover to the bisector of the opponent's available angles, which after an inside-out is 0.8-1.2 m right of the center mark",
             "Hồi vị về vạch giữa sau cú inside-out", "Thói quen hồi vị đã ghi nhớ thay vì tính toán hình học", "Phần sân trống bị lộ trước một cú chéo sân duy nhất", "Hồi vị về đường phân giác các góc khả dụng của đối thủ, sau cú inside-out là 0,8-1,2 m về phía phải vạch giữa"],
        ],
        "drills": [
            ["Inside-Out Target Ladder", "Feed short balls to the ad side; score only inside-out forehands landing in a 2 m corner zone", "Thang Mục Tiêu Inside-Out", "Tung bóng ngắn về phía ô ad; chỉ tính điểm những cú forehand inside-out rơi trong vùng góc 2 m"],
            ["Run-Around Recovery Pattern", "Execute inside-out, then recover to the bisector and play the next ball", "Mẫu Hồi Vị Sau Chạy Vòng", "Thực hiện inside-out, rồi hồi vị về đường phân giác và đánh bóng kế tiếp"],
        ],
    },
    "148": {
        "topic_en": "the jamming ball spinal disruption strategy",
        "topic_vi": "chiến lược bóng chèn phá vỡ trục cột sống",
        "mech_en": "The jamming ball targets the **rotation axis** rather than the court space. By placing the ball at the opponent's hip or non-dominant shoulder, the pattern forces the trunk to rotate around an axis the player cannot fully organize, so the resulting stroke is assembled from compensatory segments instead of a kinetic chain. The ball does not need pace to be effective; it needs **axial interference**.",
        "mech_vi": "Bóng chèn nhắm vào **trục xoay** thay vì vào khoảng không gian trên sân. Bằng cách đặt bóng ở hông hoặc vai không thuận của đối thủ, mẫu này buộc thân người phải xoay quanh một trục mà người chơi không thể tổ chức trọn vẹn, nên cú đánh tạo thành từ các phân đoạn bù trừ thay vì từ một chuỗi động lực học. Bóng không cần tốc độ để hiệu quả; nó cần **giao thoa trục**.",
        "vars": [
            ["Jam Target Offset from Hip Line", "Độ lệch mục tiêu chèn so với đường hông", "0.15-0.35 m"],
            ["Trunk Rotation Deficit Induced", "Mức thiếu hụt xoay thân gây ra", "22-35 degrees"],
            ["Ball Speed Required", "Tốc độ bóng cần thiết", "85-105 km/h"],
        ],
        "subs": [
            [
                "Axial Anatomy: Why the Hip Ball Works",
                "Giải Phẫu Trục: Vì Sao Bóng Vào Hông Hiệu Quả",
                "Trunk rotation in a groundstroke is organized around the thoracolumbar fascia and the crossed sling of the internal and external obliques. A ball placed within 0.15-0.35 m of the hip line arrives inside the space needed to organize that rotation, so the player must either step away (losing time) or swing with a truncated kinetic chain, which typically reduces racket-head speed by 18-28%.",
                "Xoay thân trong cú đánh nền được tổ chức quanh mạc ngực-thắt lưng và dây chéo của cơ chéo trong và chéo ngoài. Một quả bóng được đặt trong khoảng 0,15-0,35 m tính từ đường hông sẽ tới ngay bên trong không gian cần thiết để tổ chức xoay đó, nên người chơi buộc phải bước ra xa (mất thời gian) hoặc vung với chuỗi động lực bị cắt ngắn, thường làm giảm 18-28% tốc độ đầu vợt.",
            ],
            [
                "Sequencing the Jam: Setup, Delivery, Follow-Through",
                "Trình Tự Hóa Bóng Chèn: Chuẩn Bị, Đưa Bóng, Kết Thúc",
                "The jam is rarely a standalone shot; it is the second ball of a pattern. The first ball displaces the opponent laterally, and the jam is delivered while the opponent's hips are still resolving the recovery. Delivered from a static position, the jam is a low-value ball because the opponent can step around it with time to spare.",
                "Bóng chèn hiếm khi là một cú đánh độc lập; nó là quả bóng thứ hai của một mẫu. Quả bóng đầu tiên đẩy đối thủ lệch ngang, và bóng chèn được đưa tới trong khi hông đối thủ còn đang giải quyết pha hồi vị. Nếu đưa từ thế tĩnh, bóng chèn là một quả bóng giá trị thấp vì đối thủ có thể bước vòng qua nó với thời gian dư.",
            ],
        ],
        "steps": [
            ["Displace First, Jam Second", "The jam must be preceded by a ball that moves the opponent 2.0 m or more from their preferred contact position; a jam from a static opponent is a free ball."],
            ["Aim at the Hip Line, Not the Body", "Target 0.15-0.35 m to the non-dominant side of the hip line; the body is too large a target and produces a comfortable, organized swing."],
            ["Đẩy Lệch Trước, Chèn Sau", "Bóng chèn phải được đi trước bằng một quả bóng làm đối thủ di chuyển từ 2,0 m trở lên khỏi vị trí tiếp xúc ưa thích; chèn vào một đối thủ đang tĩnh là tặng bóng."],
            ["Nhắm Vào Đường Hông, Không Nhắm Vào Thân", "Nhắm 0,15-0,35 m về phía không thuận của đường hông; thân người là mục tiêu quá lớn và tạo ra một động tác thoải mái, có tổ chức."],
        ],
        "errs": [
            ["Jamming from a static opponent position", "The pattern is used as a first strike rather than as a second ball", "The opponent steps around the ball with time to spare and produces an offensive forehand", "Always precede the jam with a displacement ball; the jam's value is entirely derived from the opponent's unresolved hip position",
             "Chèn bóng khi đối thủ đang ở thế tĩnh", "Mẫu được dùng như cú tấn công đầu thay vì quả bóng thứ hai", "Đối thủ bước vòng qua bóng với thời gian dư và tạo ra cú forehand tấn công", "Luôn đưa một quả bóng đẩy lệch trước cú chèn; giá trị của cú chèn hoàn toàn đến từ vị thế hông chưa được giải quyết của đối thủ"],
            ["Using excessive pace on the jam", "Pace is assumed to be the mechanism of disruption", "The ball rebounds too fast to be controlled and often lands mid-court as a sitter", "Keep the jam at 85-105 km/h with heavy spin; the disruption mechanism is axial interference, not velocity",
             "Dùng quá nhiều tốc độ cho cú chèn", "Tốc độ bị giả định là cơ chế gây nhiễu loạn", "Bóng bật lại quá nhanh để kiểm soát và thường rơi giữa sân thành bóng dễ ăn", "Giữ cú chèn ở 85-105 km/h với xoáy nặng; cơ chế gây nhiễu loạn là giao thoa trục, không phải tốc độ"],
        ],
        "drills": [
            ["Displace-Then-Jam Pattern", "Hit a wide ball, then jam the hip line on the next ball; count how often the opponent cannot organize rotation", "Mẫu Đẩy Lệch Rồi Chèn", "Đánh một bóng rộng, rồi chèn vào đường hông ở quả kế tiếp; đếm số lần đối thủ không thể tổ chức xoay"],
            ["Hip-Line Target Zone", "Place a 0.4 m target at the opponent's non-dominant hip line; score hits inside it", "Vùng Mục Tiêu Đường Hông", "Đặt mục tiêu 0,4 m ở đường hông không thuận của đối thủ; tính điểm những cú vào trong vùng đó"],
        ],
    },
    "149": {
        "topic_en": "asymmetric pressure application",
        "topic_vi": "áp lực bất đối xứng",
        "mech_en": "Asymmetric pressure means concentrating repeated balls into **one constrained region** until the opponent's movement solution becomes predictable, then attacking the space that constraint creates. It is the tactical equivalent of overloading one joint: the opponent's compensation pattern becomes readable, and reading it is worth more than any single shot's quality.",
        "mech_vi": "Áp lực bất đối xứng nghĩa là dồn liên tục các quả bóng vào **một vùng bị ràng buộc** cho tới khi lời giải di chuyển của đối thủ trở nên dự đoán được, rồi tấn công khoảng trống mà ràng buộc đó tạo ra. Đây là tương đương chiến thuật của việc quá tải một khớp: mẫu bù trừ của đối thủ trở nên đọc được, và đọc được nó có giá trị hơn chất lượng của bất kỳ cú đánh đơn lẻ nào.",
        "vars": [
            ["Repetition Threshold for Constraint", "Ngưỡng lặp lại để tạo ràng buộc", "4-6 consecutive balls"],
            ["Target Zone Width", "Độ rộng vùng mục tiêu", "2.0-3.0 m"],
            ["Exploitation Window", "Cửa sổ khai thác", "1.2-1.8 s"],
        ],
        "subs": [
            [
                "Constraint Logic: Overloading a Single Solution",
                "Logic Ràng Buộc: Quá Tải Một Lời Giải Duy Nhất",
                "The opponent's movement is a solution space. Repeated balls into one 2.0-3.0 m zone eliminate most of that space, forcing a single repeated solution. Once the solution repeats four to six times, its timing and direction become statistically predictable, and the exploitable space appears as a direct consequence of the constraint rather than as a lucky opening.",
                "Di chuyển của đối thủ là một không gian lời giải. Những quả bóng lặp lại vào một vùng 2,0-3,0 m loại bỏ phần lớn không gian đó, buộc chỉ còn một lời giải lặp lại. Khi lời giải lặp lại bốn tới sáu lần, nhịp và hướng của nó trở nên dự đoán được về mặt thống kê, và khoảng trống khai thác xuất hiện như hệ quả trực tiếp của ràng buộc thay vì như một cơ hội may mắn.",
            ],
            [
                "Directional Bias and the Cost of Switching",
                "Thiên Lệch Hướng & Chi Phí Chuyển Hướng",
                "Every switch of attack direction costs the attacker 0.2-0.4 s of preparation and the defender 0.3-0.6 s of repositioning. Asymmetric pressure exploits this by making the attacker's switches infrequent and the defender's adjustments constant, so the cost accumulates on one side of the exchange.",
                "Mỗi lần chuyển hướng tấn công làm người tấn công mất 0,2-0,4 giây chuẩn bị và người phòng thủ mất 0,3-0,6 giây tái định vị. Áp lực bất đối xứng khai thác điều này bằng cách làm cho số lần chuyển hướng của người tấn công ít và số lần điều chỉnh của người phòng thủ nhiều, nên chi phí tích lũy về một phía của pha bóng.",
            ],
        ],
        "steps": [
            ["Declare the Constrained Zone", "Choose a single 2.0-3.0 m zone before the point and hold it for a minimum of four balls; switching earlier resets the constraint the opponent has begun to internalize."],
            ["Track the Opponent's Solution", "Verbally name the opponent's repeated movement solution (for example slide-and-block) so that the exploitation decision is conscious rather than instinctive."],
            ["Tuyên Bố Vùng Bị Ràng Buộc", "Chọn một vùng 2,0-3,0 m trước điểm và giữ nó tối thiểu bốn quả bóng; chuyển hướng sớm hơn sẽ đặt lại ràng buộc mà đối thủ đã bắt đầu nội hóa."],
            ["Theo Dõi Lời Giải Của Đối Thủ", "Gọi tên thành lời lời giải di chuyển lặp lại của đối thủ (ví dụ trượt và chặn) để quyết định khai thác trở nên có ý thức thay vì theo bản năng."],
        ],
        "errs": [
            ["Switching direction before the constraint is established", "Impatience; the opening is attacked while still hypothetical", "The opponent's compensation pattern never stabilizes and the point becomes a coin flip", "Hold the constrained zone for a minimum of four balls before switching; the discipline of repetition is the tactic",
             "Chuyển hướng trước khi ràng buộc được thiết lập", "Thiếu kiên nhẫn; khoảng trống bị tấn công khi còn là giả thuyết", "Mẫu bù trừ của đối thủ không bao giờ ổn định và điểm bóng trở thành may rủi", "Giữ vùng ràng buộc tối thiểu bốn quả bóng trước khi chuyển; kỷ luật lặp lại chính là chiến thuật"],
            ["Confusing pressure with pace", "Speed is treated as the mechanism of pressure", "Unforced errors accumulate while the opponent's movement solution remains untested", "Pressure is created by repetition and depth, not speed; target 2.0-3.0 m zones at 70-80% of maximum pace",
             "Nhầm áp lực với tốc độ", "Tốc độ bị coi là cơ chế của áp lực", "Lỗi tự đánh bại tích lũy trong khi lời giải di chuyển của đối thủ vẫn chưa bị thử thách", "Áp lực được tạo bằng sự lặp lại và chiều sâu, không bằng tốc độ; nhắm vùng 2,0-3,0 m ở 70-80% tốc độ tối đa"],
        ],
        "drills": [
            ["Four-Ball Constraint Set", "Play points requiring at least four consecutive balls into the declared zone before any switch", "Set Ràng Buộc Bốn Bóng", "Chơi điểm bóng yêu cầu ít nhất bốn quả liên tiếp vào vùng đã tuyên bố trước khi được chuyển hướng"],
            ["Solution Naming", "Partner calls out the opponent's repeated movement solution after each rally", "Gọi Tên Lời Giải", "Đồng đội gọi tên lời giải di chuyển lặp lại của đối thủ sau mỗi pha bóng"],
        ],
    },
    "150": {
        "topic_en": "non-linear timing disruption",
        "topic_vi": "phá vỡ nhịp thời gian phi tuyến tính",
        "mech_en": "Non-linear timing disruption attacks the opponent's **rhythm prediction** rather than their position. By varying the interval between your contacts by 0.15-0.45 s while holding ball quality constant, you prevent the opponent's motor system from settling into an anticipatory cadence, which raises their effective reaction time and degrades the quality of their first step.",
        "mech_vi": "Phá vỡ nhịp thời gian phi tuyến tính tấn công **khả năng dự đoán nhịp** của đối thủ thay vì vị trí của họ. Bằng cách thay đổi khoảng thời gian giữa các lần tiếp xúc của bạn 0,15-0,45 giây trong khi giữ nguyên chất lượng bóng, bạn ngăn hệ vận động của đối thủ ổn định vào một nhịp dự đoán trước, làm tăng thời gian phản ứng hiệu dụng và làm suy giảm chất lượng bước chân đầu tiên của họ.",
        "vars": [
            ["Inter-Contact Interval Variance", "Phương sai khoảng thời gian giữa các lần tiếp xúc", "0.15-0.45 s"],
            ["Ball Quality Held Constant", "Chất lượng bóng được giữ không đổi", "depth above 6.0 m"],
            ["Opponent Reaction Penalty", "Mức phạt phản ứng của đối thủ", "40-90 ms"],
        ],
        "subs": [
            [
                "Rhythm Entrainment and Its Collapse",
                "Sự Cuốn Nhịp & Sự Sụp Đổ Của Nó",
                "The motor system entrains to periodic input; when intervals are stable, anticipation improves and reaction time falls. Introducing controlled variance in the inter-contact interval breaks entrainment and forces genuine reaction. The key constraint is that variance must be applied to timing only, because varying ball quality as well converts a tactical weapon into an error generator.",
                "Hệ vận động bị cuốn vào đầu vào có chu kỳ; khi các khoảng thời gian ổn định, khả năng dự đoán trước được cải thiện và thời gian phản ứng giảm. Việc đưa phương sai có kiểm soát vào khoảng thời gian giữa các lần tiếp xúc phá vỡ sự cuốn nhịp và buộc phải phản ứng thật. Ràng buộc then chốt là phương sai chỉ được áp dụng cho nhịp, vì thay đổi cả chất lượng bóng sẽ biến vũ khí chiến thuật thành máy tạo lỗi.",
            ],
            [
                "Height and Spin as Timing Modulators",
                "Độ Cao & Xoáy Như Bộ Điều Chế Nhịp",
                "Ball height and spin are the two legitimate levers for changing the opponent's available preparation time without changing your own risk. A 0.4 m increase in bounce height adds roughly 60-110 ms of opponent preparation time, while heavy topspin adds another 40-80 ms of contact difficulty. Alternating these two levers is the practical mechanism of non-linear disruption.",
                "Độ cao bóng và xoáy là hai đòn bẩy chính đáng để thay đổi thời gian chuẩn bị khả dụng của đối thủ mà không thay đổi rủi ro của chính bạn. Tăng 0,4 m độ cao nảy cộng thêm khoảng 60-110 mili giây thời gian chuẩn bị cho đối thủ, trong khi topspin nặng cộng thêm 40-80 mili giây độ khó tiếp xúc. Luân phiên hai đòn bẩy này là cơ chế thực tiễn của việc phá vỡ nhịp phi tuyến tính.",
            ],
        ],
        "steps": [
            ["Hold Depth, Vary Interval", "Before varying anything, verify that depth stays above 6.0 m for ten consecutive balls; timing variance on top of inconsistent depth produces errors, not pressure."],
            ["Change One Lever at a Time", "Alternate between a high heavy ball and a lower driving ball; changing both height and pace in the same sequence removes the opponent's reference frame and your own."],
            ["Giữ Chiều Sâu, Thay Đổi Khoảng Nhịp", "Trước khi thay đổi bất cứ điều gì, xác minh chiều sâu vẫn trên 6,0 m trong mười quả liên tiếp; phương sai nhịp trên nền chiều sâu không ổn định tạo ra lỗi, không tạo ra áp lực."],
            ["Đổi Một Đòn Bẩy Mỗi Lần", "Luân phiên giữa một bóng cao nặng và một bóng thấp tấn công; đổi cả độ cao lẫn tốc độ trong cùng một trình tự sẽ loại bỏ hệ quy chiếu của đối thủ và cả của chính bạn."],
        ],
        "errs": [
            ["Varying ball quality instead of timing", "Disruption is attempted by changing pace and depth simultaneously", "Unforced errors rise faster than the opponent's reaction penalty", "Freeze depth and pace; vary only the interval and the bounce height, and re-verify depth every ten balls",
             "Thay đổi chất lượng bóng thay vì thay đổi nhịp", "Việc phá nhịp được thực hiện bằng cách đổi tốc độ và chiều sâu cùng lúc", "Lỗi tự đánh bại tăng nhanh hơn mức phạt phản ứng của đối thủ", "Cố định chiều sâu và tốc độ; chỉ thay đổi khoảng nhịp và độ cao nảy, và kiểm chứng lại chiều sâu mỗi mười quả"],
            ["Disrupting rhythm in a pattern the opponent enjoys", "Timing variance is applied without regard to the opponent's preferred tempo", "The opponent's preparation improves because the variance matches their natural cadence", "Identify whether the opponent prefers fast or slow cadence and apply variance in the opposite direction",
             "Phá nhịp trong một mẫu mà đối thủ ưa thích", "Phương sai nhịp được áp dụng không xét tới nhịp độ ưa thích của đối thủ", "Sự chuẩn bị của đối thủ tốt lên vì phương sai khớp với nhịp tự nhiên của họ", "Xác định đối thủ thích nhịp nhanh hay chậm và áp dụng phương sai theo hướng ngược lại"],
        ],
        "drills": [
            ["Interval Variance Rally", "Rally with a partner while a coach signals interval changes every three balls", "Pha Bóng Biến Thiên Nhịp", "Đánh qua lại với đồng đội trong khi huấn luyện viên ra tín hiệu đổi nhịp mỗi ba quả bóng"],
            ["Height Alternation Ladder", "Alternate high heavy and low driving balls, scoring only sequences of six with depth maintained", "Thang Luân Phiên Độ Cao", "Luân phiên bóng cao nặng và bóng thấp tấn công, chỉ tính điểm chuỗi sáu quả giữ được chiều sâu"],
        ],
    },
}
