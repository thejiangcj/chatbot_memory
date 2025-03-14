import requests
import streamlit as st

# 设置标题和描述
st.title("💬 你的喜好我都记得")
st.caption("🚀 带有长期记忆的聊天哦")

# 获取最新的记忆数据（从 FastAPI 获取）
def get_memories():
    try:
        response = requests.get("http://localhost:8000/memories")  # 调用获取所有记忆的 API
        if response.status_code == 200:
            return response.json().get("memories", [])
        else:
            st.error("Error: Unable to fetch memories from the backend.")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return []

# 初始化聊天记录和记忆
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 初始化 mem_changed 标志，默认值为 False
mem_changed = False

# 在侧边栏显示记忆数据，只更新一次，避免重复渲染
if "memories" not in st.session_state:
    st.session_state["memories"] = get_memories()  # 初始加载时获取记忆

# 显示侧边栏的输入选项
with st.sidebar:
    # 对话模型下拉框
    dialog_model = st.selectbox("对话模型", ["moonshot", "deepseek"])
    
    # 记忆模型下拉框
    memory_model = st.selectbox("记忆抽取模型", ["qwen", "deepseek"])
    
    # 人设文本输入框
    persona = st.text_area("人设", "请你扮演一个小狗狗和我说话，注意语气可爱、亲密，叫我“主人”，喜欢用emoji", height=100)
    
    # 频率输入框
    frequency = st.number_input("记忆抽取频率", min_value=1, max_value=10, step=1, value = 1)
    
    # 记忆阈值输入框
    memory_threshold = st.number_input("输入记忆阈值", min_value=0.0, max_value=1.0, step=0.01, value=0.6)

# 显示聊天记录
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 用户输入
if prompt := st.chat_input():
    # 显示用户输入
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 向自定义 API 发送请求，获取聊天回复
    try:
        # 发送所有用户选择的数据和输入内容到后端
        response = requests.post(
            "http://localhost:8000/chat",  # API 地址
            json={
                "content": prompt,
                "dialog_model": dialog_model,
                "memory_model": memory_model,
                "persona": persona,
                "frequency": frequency,
                "memory_threshold": memory_threshold
            }
        )
        if response.status_code == 200:
            json_response = response.json()
            bot_reply = json_response.get("reply", "No response from API.")
            mem_changed = json_response.get("has_mem", False)
            
            if mem_changed:
                bot_reply = bot_reply + "\n\n" + "[记忆已更新]"
                
                # 如果记忆更新，重新获取最新的记忆，并增量更新 session_state["memories"]
                new_memories = get_memories()
                
                # 只增加新的记忆项，而不是完全覆盖
                if new_memories != st.session_state["memories"]:
                    st.session_state["memories"] = new_memories
                    # 只在记忆变化时更新侧边栏
                    st.sidebar.json(st.session_state["memories"])  # 更新侧边栏的记忆展示
            
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            st.chat_message("assistant").write(bot_reply)
        else:
            st.error("Error: Unable to fetch response from the backend.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")

# 显示初始的记忆数据（如果没有变化）
if "memories" in st.session_state and not mem_changed:
    st.sidebar.json(st.session_state["memories"])  # 只显示当前存储的记忆
