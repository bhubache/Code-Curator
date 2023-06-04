import os
import re

root_code_dir: str = os.path.join('/', 'home', 'brandon', 'ManimCS', 'Code_Curator', 'src', 'code_curator')
top_level_modules: list[str] = [module.replace('.py', '').strip() for module in os.listdir(root_code_dir)]

print(top_level_modules)


for root, subdirs, files in os.walk(root_code_dir):
    for file in files:
        if not file.endswith('.py'):
            continue

        with open(os.path.join(root, file), 'r+') as file_to_change:
            contents: str = file_to_change.read()

            for module in top_level_modules:
                contents = re.sub(rf'(?!from code_curator)from {module}', rf'from code_curator.{module}', contents)
            
            file_to_change.seek(0)
            file_to_change.write(contents)
            file_to_change.truncate()

print('Done!')
