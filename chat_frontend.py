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
        response = requests.post(
            "http://localhost:8000/chat",  # API 地址
            json={"content": prompt}
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