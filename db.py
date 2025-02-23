# db.py

def save_to_db(content: str):
    """将数据追加到 memory.txt 文件中，每次存储新的一行"""
    try:
        with open("memory.txt", "a", encoding="utf-8") as file:
            file.write(content + "\n")  # 追加一行内容
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error saving data to db: {e}")

def get_all_db():
    """从 memory.txt 文件中读取所有行，每行作为一条数据"""
    try:
        with open("memory.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()  # 读取所有行
            # 清理每一行的换行符
            lines = [line.strip() for line in lines]
        
        print(f"读取到 {len(lines)} 条记忆数据。")  # 打印读取的行数
        return lines
    
    except Exception as e:
        print(f"Error reading data from db: {e}")
        return []  # 如果读取失败，返回空列表

# 测试函数
if __name__ == "__main__":
    # test_content = "这是一条测试内容"
    # save_to_db(test_content)
    
    # 读取并打印所有内容
    memories = get_all_db()
    for memory in memories:
        print(f"记忆内容: {memory}")