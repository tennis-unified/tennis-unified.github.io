import subprocess, re, os

SLUG = '18-tennis-groundstroke-out-steps'
EN_PATH = f'fundamentals/footwork/{SLUG}/index.html'
VI_PATH = f'vi/fundamentals/footwork/{SLUG}/index.html'
EN_CANON = f'/fundamentals/footwork/{SLUG}/'
VI_CANON = f'/vi/fundamentals/footwork/{SLUG}/'
VI_TITLE = '18 Bước "Out-Steps" (Di Chuyển Ra Ngoài) Cú Groundstroke Trong Tennis — Thư Viện Tennis Unified'

# Faithful Vietnamese translation. Structure mirrors the EN article exactly:
# same tags, same Facebook/YouTube iframes, same image (root-absolute src), same TP-NAV links.
VI_BODY = '''


<h1 id="18-tennis-groundstroke-out-steps">18 Bước "Out-Steps" (Di Chuyển Ra Ngoài) Cú Groundstroke Trong Tennis<a class="headerlink" href="#18-tennis-groundstroke-out-steps" title="Permanent link"></a></h1>
<p><strong>David Bailey</strong></p>

<div class="tp-video-embed">
<iframe src="https://www.facebook.com/plugins/video.php?href=https://www.facebook.com/videos/2509257629592193&width=1280" width="100%" height="720" frameborder="0" allowfullscreen></iframe>
</div>

<p>18 Bước "Out-Steps" (Di Chuyển Ra Ngoài) Cú Groundstroke Trong Tennis -</p><p><img src="/assets/images/groundstroke-velocities-soar-in-pro-tennis__image9.jpeg" alt="18 Bước Out-Steps Cú Groundstroke" style="max-width:100%; height:auto; border-radius:8px; box-shadow: 0 4px 16px rgba(0,0,0,.15); margin: 1.5rem 0;" /></p>
<p>Các biến thể di chuyển lùi, di chuyển ngang và chạy vòng trước khi thiết lập "Tư Thế Đánh" (Hitting Stance)</p>
<p>Đầu tiên …"Out-Steps" là gì?</p>
<p>Đơn giản …đó là một bước hoặc tổ hợp các bước mà người chơi thực hiện để di chuyển "ra ngoài" đón quả bóng đang tới và đứng trước tư thế đánh!</p>
<p>Các Out-Steps cũng xác định cách gọi tên cho Cú Di Chuyển Tiếp Xúc (Contact Move) được chọn</p>
<p>Cụ thể …Một "Low Step Down with Rhythm" Out-Steps hoặc một "Power Move" với các bước chạy</p>
<p>Quan trọng: Đừng bỏ qua tầm quan trọng của những Bước Đầu Tiên ……</p>
<p>Tôi thường nói "Nếu bạn sửa được "Out-Steps", bạn sẽ sửa được nhịp độ và khoảng cách của cú đánh của mình!"</p>
<p><strong>Nguồn:</strong> <a href="https://www.facebook.com/tennisfootwork/videos/2509257629592193/">Xem trên Bailey Tennis Footwork (Facebook)</a></p>
<p>Ghé thăm website của David! <a href="http://www.baileytennisfootwork.com/"><strong>[!]</strong></a></p>
<p>Liên hệ trực tiếp với David <a href="mailto:david@baileytennisfootwork.com"><strong>[!]</strong></a></p>





<div class="video-container">
  <iframe src="https://www.youtube.com/embed/qdyBAG86tac?rel=0" width="100%" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen height="100%"></iframe>
</div>

<!-- TP-NAV-START -->

<!-- TP-NAV-START -->
<hr />
<p style="text-align:center; margin:2rem 0; font-size:0.95rem;">
<a href="../the-bailey-method-overview/"> Phương Pháp Bailey — Tổng Quan</a> &nbsp;|&nbsp; <a href="../"> Trang Chủ Footwork</a> &nbsp;|&nbsp; <a href="../5-steps-to-master-your-footwork/">5-steps-to-master-your-footwork </a>
</p>
<!-- TP-NAV-END -->
'''

en_html = subprocess.check_output(['git','show',f'HEAD:{EN_PATH}'], text=True, errors='replace')

# ---- Build VI page ----
vi_html = en_html
# VI page is exactly one directory level deeper than EN, so every root-relative
# "../../../" must become "../../../../" (4 ups WITH trailing slash) to keep
# resolving to repo root. (A trailing slash is essential: "../../../" + "assets"
# must become "../../../../assets", NOT "../../../..assets".)
vi_html = vi_html.replace('../../../', '../../../../')
vi_html = re.sub(r'(<html[^>]*)lang="en"', r'\1lang="vi"', vi_html)
vi_html = vi_html.replace('<title>'+re.search(r'<title>(.*?)</title>', en_html, re.S).group(1)+'</title>',
                           '<title>'+VI_TITLE+'</title>')
vi_html = vi_html.replace('<link rel="canonical" href="'+EN_CANON+'">',
                           '<link rel="canonical" href="'+VI_CANON+'">')
# alternates: en + x-default currently both "./"
vi_html = vi_html.replace('<link rel="alternate" href="./" hreflang="en">',
                           '<link rel="alternate" href="'+EN_CANON+'" hreflang="en">')
vi_html = vi_html.replace('<link rel="alternate" href="./" hreflang="x-default">',
                           '<link rel="alternate" href="'+EN_CANON+'" hreflang="x-default">')
vi_html = vi_html.replace('<link rel="alternate" href="'+EN_CANON+'" hreflang="en">',
                           '<link rel="alternate" href="'+VI_CANON+'" hreflang="vi">\n<link rel="alternate" href="'+EN_CANON+'" hreflang="en">')
# switcher in VI body: EN link -> EN canon, VI link (currently overview) -> self "./"
vi_html = vi_html.replace('<a href="./" hreflang="en"', '<a href="'+EN_CANON+'" hreflang="en"')
vi_html = re.sub(r'<a href="[^"]*the-12-golden-moves-an-overview[^"]*" hreflang="vi"',
                 '<a href="./" hreflang="vi"', vi_html)
# replace article body
vi_html = re.sub(r'(<article[^>]*>)(.*?)(</article>)', lambda m: m.group(1)+VI_BODY+m.group(3), vi_html, flags=re.S)

# ---- Update EN page: add vi alternate + fix VI switcher href ----
en_upd = en_html
en_upd = en_upd.replace('<link rel="alternate" href="./" hreflang="en">',
                         '<link rel="alternate" href="'+VI_CANON+'" hreflang="vi">\n<link rel="alternate" href="./" hreflang="en">')
en_upd = re.sub(r'<a href="[^"]*the-12-golden-moves-an-overview[^"]*" hreflang="vi"',
                '<a href="'+VI_CANON+'" hreflang="vi"', en_upd)

# sanity: ensure image src is root-absolute in VI body
assert '/assets/images/groundstroke-velocities' in VI_BODY

# write files (create VI directory first)
os.makedirs(os.path.dirname(VI_PATH), exist_ok=True)
with open(VI_PATH, 'w', encoding='utf-8') as f: f.write(vi_html)
with open(EN_PATH, 'w', encoding='utf-8') as f: f.write(en_upd)
print("VI page written:", VI_PATH, len(vi_html), "bytes")
print("EN page updated:", EN_PATH, len(en_upd), "bytes")
# quick self-checks
print("VI lang:", 'lang="vi"' in vi_html, "| EN lang:", 'lang="en"' in en_upd)
print("VI has vi alternate:", ('hreflang="vi"' in vi_html), "| EN has vi alternate:", ('hreflang="vi"' in en_upd))
print("VI img root-absolute:", VI_CANON in vi_html and '/assets/images/groundstroke' in vi_html)
print("VI switcher self VI:", 'href="./" hreflang="vi"' in vi_html)
print("EN switcher -> VI twin:", ('href="'+VI_CANON+'" hreflang="vi"') in en_upd)
print("VI base len (no 3-dot left):", '../../../' not in vi_html.replace('../../../..',''))
