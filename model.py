import streamlit as st
import requests

# -------------------------- 页面配置 --------------------------
st.set_page_config(
    page_title="韦达定理 AI 教学系统",
    page_icon="📚",
    layout="wide"
)

# 初始化会话状态变量
if "video_time" not in st.session_state:
    st.session_state.video_time = 0

if "q_text" not in st.session_state:
    st.session_state.q_text = ""

st.title("📚 韦达定理 —— 一体化AI教学辅助系统")
st.markdown("### 一元二次方程根与系数的关系 | 微课学习 + AI答疑 + AI智能出题批改")

# ====================== 讯飞星火 API 配置 ======================
APIPASSWORD = "bhyQgkXwDofXpQQgeKNo:eQQdpZADNppxZSlDGmnQ"
API_URL = "https://spark-api-open.xf-yun.com/v2/chat/completions"
MODEL_NAME = "spark-x"  # 正确稳定模型名

# ====================== AI 通用调用函数 ======================
def ai_response(prompt):
    headers = {
        "Authorization": f"Bearer {APIPASSWORD}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "你是专业初中数学老师，简洁、准确、教学式回答"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    try:
        res = requests.post(API_URL, headers=headers, json=data, timeout=60)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ AI调用失败：{str(e)}"

# ====================== AI 出题 ======================
def ai_generate_question():
    prompt = """
    请出一道九年级韦达定理基础题，只包含以下三种之一：
    1. 已知方程求两根和
    2. 已知方程求两根积
    3. 已知两根求方程
    只输出题目，不要输出答案，不要多余解释。
    """
    return ai_response(prompt)

# ====================== AI 批改 ======================
def ai_check(question, user_answer):
    prompt = f"""
    题目：{question}
    学生答案：{user_answer}
    请只判断对错，正确输出【正确】，错误输出【错误，正确答案：XXX】
    不要多余解释，简洁。
    """
    return ai_response(prompt)

# -------------------------- 三大标签页 --------------------------
tab1, tab2, tab3 = st.tabs(["🎦 观看微课", "💬 AI实时答疑", "📝 AI智能出题批改"])

# ====================== 页1：视频 + 侧边AI提示（无刷新！不影响其他页面） ======================
with tab1:
    st.subheader("🎦 韦达定理速通微课")

    col_left, col_right = st.columns([2, 1])

    with col_left:
        try:
            st.video("0ca6fb4753bc462ca6745c982f5ff55b.mp4")
            start_time = st.session_state.video_time
        except:
            st.info("ℹ️ 请放入微课视频")

    with col_right:
        st.markdown("### 🤖 AI 实时提示区")
        st.markdown("---")

        slider_container = st.empty()
        with slider_container:
            st.session_state.video_time = st.slider(
                "拖动跟随视频进度",
                min_value=0,
                max_value=189,
                value=st.session_state.video_time,
                key="video_slider",
                label_visibility="visible"
            )
        # 滑块拖动 = 视频进度（无刷新、不卡死页面！）
        current_time = st.slider("拖动跟随视频进度", 0, 189, 0)  # 3分9秒=189秒

        if 62 <= current_time <= 65:
            st.success("🤖 标准形式：ax²+bx+c=0（a≠0）")
        elif 68 <= current_time <= 73:
            st.success("🤖 必须满足：Δ≥0 有实根才能使用")
        elif 90 <= current_time <= 98:
            st.error("🤖 重点：x₁+x₂ = −b/a（负号极易错）")
        elif 140 <= current_time <= 150:
            st.success("✅ 记三点：公式、Δ、标准化")
        elif 160 <= current_time <= 165:
            st.warning("🤖 易错点：忘负号｜不算Δ｜不化标准式")
        elif 180 <= current_time <= 185:
            st.info("大家还有什么疑惑的地方呢？可以移步至AI辅助教学系统答疑吧~")
        else:
            st.info("🤖 播放视频，拖动进度条同步提示")

# ====================== 页2：AI答疑（正常显示） ======================
with tab2:
    st.subheader("💬 AI实时答疑")
    st.caption("可提问：公式、易错点、Δ、推导、x₁²+x₂²等韦达定理相关问题")
    q = st.text_input("输入你的问题：")
    if st.button("🔍 提问AI老师"):
        if q.strip():
            with st.spinner("AI思考中..."):
                ans = ai_response(q)
            st.success(ans)
        else:
            st.warning("请输入问题内容")

# ====================== 页3：AI出题批改（正常显示） ======================
with tab3:
    st.subheader("📝 AI 智能出题 · AI 自动批改")

    if "q_text" not in st.session_state:
        st.session_state.q_text = ai_generate_question()

    st.info(f"**AI 出题：** {st.session_state.q_text}")
    user_ans = st.text_input("你的答案：")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ AI批改"):
            if user_ans.strip():
                with st.spinner("AI批改中..."):
                    result = ai_check(st.session_state.q_text, user_ans)
                if "正确" in result:
                    st.success("🎉 " + result)
                else:
                    st.error("❌ " + result)
            else:
                st.warning("请输入你的答案")
    with col2:
        if st.button("🔄 换一道AI新题"):
            st.session_state.q_text = ai_generate_question()
            st.rerun()

st.divider()
st.caption("© AI教学辅助系统 | 微课版")