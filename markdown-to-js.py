import os
import json
import re

def parse_md_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    name_match = re.search(r'### (.+)', content)
    name = name_match.group(1).strip() if name_match else 'Name Not Found'

    password_match = re.search(r'PASSWORD\s*=\s*"(.*?)"', content)
    password = password_match.group(1).strip() if password_match else ''

    describe_match = re.search(r'```([^`]+)```', content, re.DOTALL)
    describe = describe_match.group(1).strip().replace('\n', '<br>') if describe_match else 'Description Not Found'

    return {'name': name, 'password': password, 'describe': describe}

def generate_js_for_folder(folder_path):
    data_list = []
    for file in os.listdir(folder_path):
        if file.endswith('.md'):
            file_path = os.path.join(folder_path, file)
            md_data = parse_md_file(file_path)
            md_data['id'] = os.path.splitext(file)[0]
            md_data['mode'] = os.path.basename(folder_path)
            data_list.append(md_data)
    return data_list

def generate_js(script_dir):
    all_data = []
    folders = ['vocabulary', 'sentence', 'paragraph']
    for folder in folders:
        folder_path = os.path.join(script_dir, folder)
        if os.path.exists(folder_path):
            all_data.extend(generate_js_for_folder(folder_path))

    js_content = 'const JSONList = ' + json.dumps(all_data, indent=4, ensure_ascii=False).replace('</', '<\\/') + ';\n'
    with open(os.path.join(script_dir, 'database.js'), 'w', encoding='utf-8') as js_file:
        js_file.write(js_content)

# Use the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
generate_js(script_dir)
