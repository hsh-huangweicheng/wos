import re

files = [
    'C:/Workspace/wos/src/pages/Home.tsx',
    'C:/Workspace/wos/src/pages/StaffManage.tsx',
    'C:/Workspace/wos/src/pages/InstitutionConfig.tsx',
    'C:/Workspace/wos/src/utils/wosParser.ts',
]

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove zero-width characters and other problematic Unicode
        content = re.sub(r'[​-‏ - ﻿]', '', content)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed {filepath}')
    except Exception as e:
        print(f'Error fixing {filepath}: {e}')
