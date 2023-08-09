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
    save_config_to_file('config.json', settings)

    
# 設定ファイルを読み込む
try:
    SETTINGS_FILE = r'config.json'
    settings = load_config_from_file(SETTINGS_FILE)
except:
    DEFAULT_SETTINGS_FILE = r'./assets/config.json'
    save_config_to_file('config.json', load_config_from_file(DEFAULT_SETTINGS_FILE))
    settings = load_config_from_file(SETTINGS_FILE)
    print('config.jsonを作成したよ！')