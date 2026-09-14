import json
import re

# Read batch file
with open('C:/Users/Phamd/tennis-unified-deploy/_batch_0.json', 'r', encoding='utf-8') as f:
    batch = json.load(f)

# Article 1: backhand-slice-penetration-and-skid
art1 = batch[0]['en_article']

# Translate Article 1
vi1 = art1

# Breadcrumb
vi1 = vi1.replace(
    'Backhand Mechanics &rsaquo; <strong>Backhand Slice: Carving Low Penetration & Heavy Skid</strong>',
    'Cơ Học Trái Tay &rsaquo; <strong>Trái Tay Slice: Cắt Xuyên Thấp & Trượt Nặng</strong>'
)

# Title
vi1 = vi1.replace(
    'Backhand Slice: Carving Low Penetration & Heavy Skid',
    'Trái Tay Slice: Cắt Xuyên Thấp & Trượt Nặng'
)

# Author line
vi1 = vi1.replace('Author:', 'Tác giả:')
vi1 = vi1.replace('Source:', 'Nguồn:')

# Back link
vi1 = vi1.replace('&larr; Back to all chapters in Backhand Mechanics', '&larr; Quay lại tất cả chương trong Cơ Học Trái Tay')

# Paragraph translations
vi1 = vi1.replace(
    'The backhand slice is one of the most common shots in recreational tennis, yet in most cases the slice is floating up too high and is easy to attack.',
    'Trái tay slice là một trong những cú đánh phổ biến nhất trong tennis giải trí, nhưng trong hầu hết các trường hợp slice nổi lên quá cao và dễ bị tấn công.'
)

vi1 = vi1.replace(
    'The following backhand slice tip helps you develop that extra bite on the slice (whether backhand or forehand) and change the slice from a simple neutral shot to a more offensive one.',
    'Mẹo trái tay slice sau đây giúp bạn phát triển độ cắn thêm trên slice (dù là trái tay hay thuận tay) và thay đổi slice từ một cú đánh trung lập đơn giản thành một cú tấn công hơn.'
)

# H2
vi1 = vi1.replace(
    'The Biting Backhand Slice',
    'Trái Tay Slice Cắn Mạnh'
)

vi1 = vi1.replace(
    'The feel exercise of cutting the net is one of the final polishing techniques one needs to add to one\'s tennis backhand slice technique in order to make the slice more effective and not sit up in the air.',
    'Bài tập cảm nhận cắt lưới là một trong những kỹ thuật hoàn thiện cuối cùng cần thêm vào kỹ thuật trái tay slice tennis để làm cho slice hiệu quả hơn và không nổi lên trên không.'
)

# Imagery text
vi1 = vi1.replace(
    'Imagine "slicing" the net open with your backhand slice',
    'Tưởng tượng "cắt" lưới mở với cú trái tay slice của bạn'
)

vi1 = vi1.replace(
    'As I mentioned in the video, to add bite to your slice backhand, you should:',
    'Như tôi đã đề cập trong video, để thêm độ cắn vào trái tay slice của bạn, bạn nên:'
)

# List items
vi1 = vi1.replace(
    'Make a long cut – imagine making a meter (3–4 feet) long slice into the net;',
    'Thực hiện cú cắt dài – tưởng tượng thực hiện cú cắt dài một mét (3–4 bàn chân) vào lưới;'
)

vi1 = vi1.replace(
    'Slice the net from tape down and don\'t change the racquet path – keep it in a straight line until you stop touching the net and only then lift the racquet into the follow-through;',
    'Cắt lưới từ dải băng xuống và không thay đổi đường vợt – giữ nó trong đường thẳng cho đến khi bạn ngừng chạm lưới và chỉ sau đó nâng vợt lên vào đà hoàn thành;'
)

vi1 = vi1.replace(
    'Alternate between the feel drill of slicing the net and hitting backhand slice shots from the baseline; and',
    'Luân phiên giữa bài tập cảm nhận cắt lưới và đánh cú trái tay slice từ vạch giao bóng; và'
)

vi1 = vi1.replace(
    'Accelerate a few times with full speed as that will help you engage your whole body into the shot and feel which parts of the body you can use to generate power. Oftentimes, players are too focused on their arm movement and thus disengage the legs. The legs, hips and the trunk are the main energy sources for all shots including a backhand slice.',
    'Tăng tốc vài lần với tốc độ tối đa vì điều đó sẽ giúp bạn sử dụng toàn bộ cơ thể vào cú đánh và cảm nhận phần nào của cơ thể bạn có thể sử dụng để tạo sức mạnh. Thường thì người chơi quá tập trung vào chuyển động cánh tay và do đó không sử dụng chân. Chân, hông và thân là nguồn năng lượng chính cho tất cả các cú đánh bao gồm cả trái tay slice.'
)

# Note
vi1 = vi1.replace(
    '<strong>Note that you can use this exercise of cutting the net for your forehand slice, and it will also improve the bite on your volleys as most volleys need to be hit with a slight slice.</strong>',
    '<strong>Lưu ý rằng bạn có thể sử dụng bài tập cắt lưới này cho cú thuận tay slice của bạn, và nó cũng sẽ cải thiện độ cắn trên cú volley vì hầu hết cú volley cần được đánh với một chút slice.</strong>'
)

# More paragraphs
vi1 = vi1.replace(
    'Of course, with the extra speed of the racquet head, you will increase the risk of missing since the ball will go lower above the net and travel faster.',
    'Tất nhiên, với tốc độ thêm của đầu vợt, bạn sẽ tăng rủi ro trượt bóng vì bóng sẽ đi thấp hơn trên lưới và di chuyển nhanh hơn.'
)

vi1 = vi1.replace(
    'Therefore, it will still take you some time to master the backhand slice shot as a more offensive stroke in tennis.',
    'Do đó, vẫn sẽ mất một thời gian để làm chủ cú trái tay slice như một cú tấn công hơn trong tennis.'
)

vi1 = vi1.replace(
    'You will also need to learn when to actually apply that extra bite for more offensive situations or use a slower, floating slice when you\'re pushed out of the court and need to buy yourself time to get back in the correct recovery position.',
    'Bạn cũng cần học khi nào thực sự áp dụng độ cắn thêm đó cho các tình huống tấn công hơn hoặc sử dụng slice chậm hơn, nổi khi bạn bị đẩy ra khỏi sân và cần giành thời gian để quay lại tư thế phục hồi đúng.'
)

vi1 = vi1.replace(
    'Feel free to let me know in the comments below how this backhand slice tip worked for you!',
    'Hãy cho tôi biết trong bình luận bên dưới mẹo trái tay slice này có hiệu quả với bạn như thế nào!'
)

# Nav labels
vi1 = vi1.replace('← Previous', '← Trước')
vi1 = vi1.replace('Next →', 'Tiếp →')
vi1 = vi1.replace('Backhand Slice', 'Trái Tay Slice')
vi1 = vi1.replace('Backswing', 'Đường Vợt Lùi')
vi1 = vi1.replace('🏠 Index / Home', '🏠 Chỉ Mục / Trang Chủ')
vi1 = vi1.replace('Backhand', 'Trái Tay')

# Video card
vi1 = vi1.replace('BATCH 3 &middot; BACKHAND MASTERCLASS', 'LÔ 3 &middot; LỚP TRÁI TAY NÂNG CAO')

# Bottom nav
vi1 = vi1.replace('One Handed Backhand (1Hbh)', 'Trái Tay Một Tay (1Hbh)')
vi1 = vi1.replace('Open Stance vs Closed Stance', 'Tư Thế Mở vs Tư Thế Đóng')

print("Article 1 translated successfully")
print(f"Length: {len(vi1)} chars")

# Write Article 1
with open('C:/Users/Phamd/tennis-unified-deploy/backhand_backhand-slice-penetration-and-skid.vi.md', 'w', encoding='utf-8') as f:
    f.write(vi1)

print("Wrote: backhand_backhand-slice-penetration-and-skid.vi.md")
