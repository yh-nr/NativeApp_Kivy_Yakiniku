import json

def load_config_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def update_setting(btn, num, name):
    settings[btn]['num'] = num
    settings[btn]['name'] = name
    save_config_to_file('savetest.json', settings)

# 設定ファイルを読み込む
SETTINGS_FILE = r'./assets/config.json'
settings = load_config_from_file(SETTINGS_FILE)
