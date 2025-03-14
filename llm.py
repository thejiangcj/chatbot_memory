import time
from openai import OpenAI
from config import MOONSHOT_API_KEY, ROLEPLAY_PROMPT, UNIVERSAL_ROLEPLAY_PROMPT

def call_moonshot_llm(prompt: str, system_prompt: str = ROLEPLAY_PROMPT + UNIVERSAL_ROLEPLAY_PROMPT, model: str = "moonshot-v1-8k", retries: int = 3, delay: int = 20):
    """
    使用 Moonshot API 调用 LLM 接口，获取回复，并实现自动重试机制。

    参数：
    prompt (str): 提供给 LLM 的提示词。
    model (str): 使用的 LLM 模型名称，默认为 "moonshot-v1-8k"。
    retries (int): 重试次数，默认为 3 次。
    delay (int): 重试间隔时间，默认为 20 秒。

    返回：
    str: LLM 的回复内容，或错误消息。
    """
    # 创建 OpenAI 客户端实例
    client = OpenAI(
        api_key=MOONSHOT_API_KEY,  # 替换为实际的 API 密钥
        base_url="https://api.moonshot.cn/v1",  # Moonshot API 基本 URL
    )

    attempt = 0
    while attempt < retries:
        try:
            # 调用 Moonshot API 的 chat.completions 创建接口
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.95
            )
            
            # 返回 LLM 的回复
            return completion.choices[0].message.content
        
        except Exception as e:
            attempt += 1
            print(f"请求发生错误: {e}，正在重试... (尝试 {attempt}/{retries})")
            
            # 如果已经尝试了指定次数，退出并返回错误消息
            if attempt >= retries:
                print("重试次数已达到上限，无法处理请求。")
                return "Error: 请求失败，已尝试多次。"
            
            # 等待一段时间后再重试
            print(f"等待 {delay} 秒后重新尝试...")
            time.sleep(delay)

    # 如果没有成功返回，在重试达到上限后仍然会返回此信息
    return "Error: 请求失败，已尝试多次。"


if __name__ == "__main__":
    # 测试调用
    prompt = "醒了？"
    response = call_moonshot_llm(prompt)
    print(response)