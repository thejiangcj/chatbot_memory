from openai import OpenAI
from config import MOONSHOT_API_KEY,ROLEPLAY_PROMPT

def call_moonshot_llm(prompt: str, system_prompt: str = ROLEPLAY_PROMPT, model: str = "moonshot-v1-8k"):
    """
    使用 Moonshot API 调用 LLM 接口，获取回复。

    参数：
    prompt (str): 提供给 LLM 的提示词。
    model (str): 使用的 LLM 模型名称，默认为 "moonshot-v1-8k"。

    返回：
    str: LLM 的回复内容。
    """
    # 创建 OpenAI 客户端实例
    client = OpenAI(
        api_key=MOONSHOT_API_KEY,  # 替换为实际的 API 密钥
        base_url="https://api.moonshot.cn/v1",  # Moonshot API 基本 URL
    )

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
        # 捕获异常并返回错误信息
        print(f"请求发生错误: {e}")
        return "Error: 请求失败"


if __name__ == "__main__":
    # 测试调用
    prompt = "醒了？"
    response = call_moonshot_llm(prompt)
    print(response)