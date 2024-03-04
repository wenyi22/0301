import json

# 讀取 JSON 檔案
def load_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# 寫入 JSON 檔案
def write_json_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# 主程式
def main():
    # 讀取 JSON 檔案
    filename = 'data.json'
    json_data = load_json_file(filename)
    
    # 顯示讀取的 JSON 資料
    print("讀取的 JSON 資料：")
    print(json_data)

    # 修改資料
    # 在這裡進行你需要的資料操作

    # 寫入 JSON 檔案
    new_filename = 'new_data.json'
    write_json_file(json_data, new_filename)
    print(f"已將資料寫入至 {new_filename}")

if __name__ == "__main__":
    main()