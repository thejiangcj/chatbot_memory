from llm import *  # 假设你已经有一个名为 llm.py 的模块
from config import MEM_EXTRACTION_PROMPT  # 假设 MEM_EXTRACTION_PROMPT 是你在 config 中定义的变量

# chat_one() - 处理聊天回复并抽取记忆
# 输入：content（用户的输入）
# 输出：reply（模型的回复），has_mem（是否有记忆），memory（抽取的记忆内容）
def chat_one(content: str):
    try:
        # 获取模型的回复
        reply = call_moonshot_llm(content)
        
        # 抽取记忆
        has_mem, memory = extract_mem(content)
        
        return reply, has_mem, memory
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
        memory = call_moonshot_llm(prompt=f"用户:{content}", system_prompt=MEM_EXTRACTION_PROMPT)
        
        # 判断返回结果是否包含记忆
        if memory == "无":
            return False, ""
        else:
            return True, memory
    except Exception as e:
        # 错误处理，捕获并打印异常
        print(f"Error in extract_mem: {e}")
        return False, ""  # 出现异常时返回默认值

# 示例调用
if __name__ == "__main__":
    try:
        # 测试输入
        content = "我的生日是12月6日"
        reply, has_mem, memory = chat_one(content)
        
        print(f"模型回复: {reply}")
        print(f"是否添加记忆：{has_mem}")
        print(f"记忆内容：{memory}")
    except Exception as e:
        print(f"Error in main execution: {e}")