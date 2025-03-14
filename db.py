# db.py
from typing import List
import json
import os

DB_PATH = "memory_db.json"

def save_to_db(memories: List[str]):
    """保存记忆到数据库（追加模式）"""
    try:
        existing = get_all_db()
        existing.extend(memories)  # 注意这里修正了括号问题
        with open(DB_PATH, 'w') as f:
            json.dump(existing, f)
    except Exception as e:
        print(f"保存到数据库失败: {e}")

def replace_in_db(index: int, new_memory: str) -> bool:
    """替换指定索引的记忆条目（新增函数）"""
    try:
        memories = get_all_db()
        if index < 0 or index >= len(memories):
            return False
        
        memories[index] = new_memory
        with open(DB_PATH, 'w') as f:
            json.dump(memories, f)
        return True
    except Exception as e:
        print(f"替换记忆失败: {e}")
        return False

def get_all_db() -> List[str]:
    """获取所有记忆"""
    if not os.path.exists(DB_PATH):
        return []
    try:
        with open(DB_PATH, 'r') as f:
            return json.load(f)
    except:
        return []

def clear_db():
    """清空所有记忆"""
    try:
        with open(DB_PATH, 'w') as f:
            json.dump([], f)
    except Exception as e:
        print(f"清空数据库失败: {e}")