import os

replacements = [
    # The canonical filesystem path (used in prose / methodology)
    ('D:/Github Repos/tennis-unified/docs/', 'D:/New Tennis Knowledge/Tennis Knowledge/Tennis-Unified/TP-Archive-Site/'),
    # The repo description (used in frontmatter and prose)
    ('the tennis-unified repo', 'the Tennis-Unified intranet'),
    ('tennis-unified repo', 'Tennis-Unified intranet'),
    ('Tennis-Unified repo', 'Tennis-Unified intranet'),
]

count = 0
for root, dirs, files in os.walk('docs'):
    for fn in files:
        if not fn.endswith('.md'):
            continue
        path = os.path.join(root, fn)
        content = open(path, encoding='utf-8').read()
        new = content
        for old, newstr in replacements:
            new = new.replace(old, newstr)
        if new != content:
            open(path, 'w', encoding='utf-8').write(new)
            count += 1
print(f'Total files updated: {count}')
