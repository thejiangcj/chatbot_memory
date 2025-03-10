import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# 定义文件路径
DB_DIR = "data"  # 存储目录
DB_FILE = os.path.join(DB_DIR, "memory.txt")  # 文件路径

def save_to_db(content: list):
    """将数据追加到 memory.txt 文件中，每次存储新的一行。"""
    try:
        # 检查传入内容是否为空
        if not content:
            logger.info("传入的记忆内容为空，跳过保存操作。")
            return

        # 检查目录是否存在，如果不存在则创建
        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)

        # 如果 memory.txt 不存在，先创建它
        if not os.path.exists(DB_FILE):
            with open(DB_FILE, "w", encoding="utf-8"):
                pass  # 只是创建文件，不写内容

        # 追加内容到文件
        with open(DB_FILE, "a", encoding="utf-8") as file:
            file.writelines(f"{mem}\n" for mem in content)
        logger.info("数据保存成功。")
    
    except Exception as e:
        logger.error(f"保存数据时出错: {e}")

def get_all_db():
    """从 memory.txt 文件中读取所有行，每行作为一条数据。"""
    try:
        # 检查文件是否存在
        if not os.path.exists(DB_FILE):
            logger.info("memory.txt 文件不存在，返回空列表。")
            return []

        # 读取文件内容
        with open(DB_FILE, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file]
        
        # 检查文件是否为空
        if not lines:
            logger.info("memory.txt 文件为空，返回空列表。")
        
        logger.info(f"读取到 {len(lines)} 条记忆数据。")
        return lines
    
    except Exception as e:
        logger.error(f"读取数据时出错: {e}")
        return []  # 如果读取失败，返回空列表

def clear_db():
    """清空 memory.txt 文件的内容。"""
    try:
        # 检查文件是否存在
        if not os.path.exists(DB_FILE):
            logger.info("memory.txt 文件不存在，无需清空。")
            return

        # 清空文件内容
        with open(DB_FILE, "w", encoding="utf-8"):
            pass
        logger.info("memory.txt 文件内容已清空。")
    
    except Exception as e:
        logger.error(f"清空文件时出错: {e}")

# 测试函数
if __name__ == "__main__":
    # 测试保存功能
    test_content = ["用户叫蔡卓悦", "用户是射手座"]
    save_to_db(test_content)
    
    # 测试读取功能
    memories = get_all_db()
    for memory in memories:
        logger.info(f"记忆内容: {memory}")

    # 测试清空功能
    clear_db()