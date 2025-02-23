from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm import *  # 假设你已经有一个名为 llm.py 的模块
from config import MEM_EXTRACTION_PROMPT  # 假设 MEM_EXTRACTION_PROMPT 是你在 config 中定义的变量
from db import save_to_db, get_all_db
from bge import compute_similarity
from config import MEMORY_USE_PROMPT

# 创建 FastAPI 实例
app = FastAPI()

# 定义输入数据结构
class ChatRequest(BaseModel):
    content: str

# chat_one() - 处理聊天回复并抽取记忆
# 输入：content（用户的输入）
# 输出：reply（模型的回复），has_mem（是否有记忆），memory（抽取的记忆内容）
def chat_one(content: str):
    try:
        # 获取模型的回复
        print(f"用户输入: {content}")  # 打印用户输入
        # reply = call_moonshot_llm(content)
        reply = reply_with_memory(content)
        print(f"模型回复: {reply}")  # 打印模型回复
        
        # 抽取记忆
        has_mem, memory = extract_mem(content)
        print(f"记忆抽取结果: {'有记忆' if has_mem else '无记忆'}")  # 打印是否有记忆
        
        if has_mem:
            print(f"保存记忆到数据库: {memory}")  # 打印保存的记忆内容
            save_to_db(memory)  # 保存到 db
        else:
            print("没有找到需要保存的记忆")  # 没有记忆时的提示
        
        return reply, has_mem, memory
    
    except Exception as e:
        # 错误处理，捕获并打印异常
        print(f"Error in chat_one: {e}")
        return "抱歉，我无法处理这个请求。", False, ""  # 出现异常时返回默认值

def reply_with_memory(content: str):
    top_k = 3
    
    memory = [item[0] for item in search_mem(content, 3)]
    memory_str = "".join(memory)  # 使用 "" 来拼接列表中的元素    
    
    try:
        content = content + MEMORY_USE_PROMPT + memory_str
        reply = call_moonshot_llm(content)
        return reply
    except Exception as e:
        # 错误处理，捕获并打印异常
        print(f"Error in chat_one: {e}")
        return "抱歉，我无法处理这个请求。", False, ""  # 出现异常时返回默认值

# extract_mem() - 使用 Moonshot LLM 分析用户输入，判断是否有需要抽取的记忆
# 输入：content（用户的输入）
# 输出：has_mem（是否有记忆），memory（抽取的记忆内容）
def extract_mem(content: str):
    try:
        # 调用 LLM 获取记忆分析结果
        print(f"分析用户输入的记忆: {content}")  # 打印分析的内容
        memory = call_moonshot_llm(prompt=f"用户:{content}", system_prompt=MEM_EXTRACTION_PROMPT)
        print(f"记忆分析结果: {memory}")  # 打印分析结果
        
        # 判断返回结果是否包含记忆
        if memory == "无":
            print("没有抽取到有效的记忆")  # 没有记忆时的提示
            return False, ""
        else:
            print(f"抽取到的记忆: {memory}")  # 打印抽取到的记忆
            return True, memory
    
    except Exception as e:
        # 错误处理，捕获并打印异常
        print(f"Error in extract_mem: {e}")
        return False, ""  # 出现异常时返回默认值


# 添加一个api获取所有的memory
@app.get("/memories")
async def get_all_memories():
    try:
        memories = get_all_db()  # 从数据库获取所有记忆
        return {"memories": memories}  # 返回所有记忆
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")

    

def search_mem(content: str, top_k: int):
    
    import numpy as np
    
    print(f"搜索记忆的关键词：{content}")
    
    # 获取所有存储的记忆
    memories = get_all_db()
    
    # 计算关键词与所有记忆的相似度
    keyword = [content]  # 关键词列表
    similarity = compute_similarity(keyword, memories)  # 假设返回的是一个二维列表或numpy数组
    print(f"相似度矩阵：\n{similarity}")
    
    # 转换为 numpy 数组以便处理
    similarity = np.array(similarity).flatten()  # 假设相似度是二维的，转换为一维
    
    # 获取 top_k 个最大相似度的索引
    top_k_indices = similarity.argsort()[-top_k:][::-1]  # argsort 会返回从小到大的索引，这里我们取反来获取最大的索引
    
    print(f"最相似的 {top_k} 个记忆的索引：{top_k_indices}")
    
    # 获取对应的记忆
    top_k_memories = [memories[i] for i in top_k_indices]
    
    print(f"最相似的 {top_k} 个记忆：")
    for idx, memory in zip(top_k_indices, top_k_memories):
        print(f"记忆 {idx}: {memory} (相似度: {similarity[idx]})")
    
    # 返回最相似的记忆和相似度
    return [(memories[i], similarity[i]) for i in top_k_indices]
    
# 创建聊天接口
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # 从请求中获取用户输入的内容
        content = request.content
        print(f"收到用户请求: {content}")  # 打印收到的请求内容
        
        # 调用 chat_one 函数获取回复、是否有记忆以及记忆内容
        reply, has_mem, memory = chat_one(content)
        
        print(f"返回给用户的回复: {reply}")  # 打印返回给用户的回复
        
        # 返回模型的回复和记忆信息
        return {"reply": reply, "has_mem": has_mem, "memory": memory}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")


if __name__ == '__main__':
    result = search_mem("萨摩耶", 2)
    print(result)

