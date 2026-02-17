import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time


from config import *
from models.embedding_model import PersianEmbeddingModel
from memory.vector_store import RealityMemory
from models.llm_interface import LLMInterface
from utils.reality_tracker import RealityTracker


# ============================================
# تنظیمات صفحه Streamlit
# ============================================
st.set_page_config(
    page_title="دستیار تحول شناختی",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# اضافه کردن CSS برای راست‌چین (فارسی)
st.markdown("""
<style>
    .stApp {
        direction: rtl;
    }
    .main-header {
        text-align: center;
        color: #2c3e50;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .reality-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-right: 5px solid #667eea;
        margin-bottom: 1rem;
    }
    .emotion-tag {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }
    .happy { background-color: #d4edda; color: #155724; }
    .sad { background-color: #f8d7da; color: #721c24; }
    .confused { background-color: #fff3cd; color: #856404; }
    .curious { background-color: #d1ecf1; color: #0c5460; }
</style>
""", unsafe_allow_html=True)


# ============================================
# کش کردن مدل‌ها برای اجرای یک‌بار (مهم برای Streamlit)
# ============================================
@st.cache_resource
def load_models():
    """بارگذاری مدل‌ها - فقط یک بار اجرا می‌شود"""
    with st.spinner("در حال بارگذاری مدل‌های هوش مصنوعی..."):
        embedding_model = PersianEmbeddingModel(EMBEDDING_MODEL)
        memory = RealityMemory(CHROMA_PERSIST_DIR, COLLECTION_NAME)
        llm = LLMInterface(OPENAI_API_KEY, USE_LOCAL_LLM)
        tracker = RealityTracker(SIMILARITY_THRESHOLD)
        
        # بارگذاری پرامپت‌ها
        try:
            with open('prompts/system_prompt.txt', 'r', encoding='utf-8') as f:
                system_prompt = f.read()
        except:
            system_prompt = "شما یک دستیار تحول شناختی هستید."
            
    return embedding_model, memory, llm, tracker, system_prompt


# بارگذاری مدل‌ها
embedding_model, memory, llm, tracker, system_prompt = load_models()


# ============================================
# مدیریت state جلسه (Session State)
# ============================================
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


if 'reality_history' not in st.session_state:
    st.session_state.reality_history = []


# ============================================
# سایدبار: تنظیمات و تاریخچه
# ============================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
    st.title("🧠 دستیار تحول شناختی")
    st.markdown("---")
    
    # اطلاعات کاربر
    st.subheader("👤 اطلاعات کاربر")
    st.text_input("نام کاربری", value=st.session_state.user_id, key="user_id_input")
    
    # دکمه شروع مکالمه جدید
    if st.button("🔄 شروع مکالمه جدید", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.reality_history = []
        st.rerun()
    
    st.markdown("---")
    
    # نمایش تاریخچه واقعیت‌ها (اگر وجود داشته باشد)
    if st.session_state.reality_history:
        st.subheader("📊 تاریخچه واقعیت‌ها")
        
        # تبدیل به DataFrame برای نمایش
        df = pd.DataFrame(st.session_state.reality_history)
        if not df.empty and 'timestamp' in df.columns:
            df['time'] = pd.to_datetime(df['timestamp']).dt.strftime('%H:%M')
            
            # نمودار تغییرات عاطفی
            if 'emotional_state' in df.columns:
                emotion_counts = df['emotional_state'].value_counts()
                fig = px.pie(
                    values=emotion_counts.values,
                    names=emotion_counts.index,
                    title="توزیع حالات عاطفی",
                    color_discrete_sequence=px.colors.sequential.Purpor
                )
                st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.caption("🌟 نسخه آزمایشی - طراحی شده برای کشف واقعیت‌های پویا")


# ============================================
# صفحه اصلی
# ============================================
st.markdown('<div class="main-header"><h1>🧠 دستیار تحول شناختی</h1><p>همراه شما در سفر کشف واقعیت‌های جدید</p></div>', unsafe_allow_html=True)


# ایجاد دو ستون
col1, col2 = st.columns([2, 1])


with col1:
    st.subheader("💬 گفتگو با دستیار")
    
    # نمایش تاریخچه گفتگو
    chat_container = st.container(height=400)
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="background-color: #e3f2fd; padding: 0.5rem 1rem; border-radius: 15px; margin-bottom: 0.5rem; text-align: right;">
                    <b>شما:</b> {msg['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: #f3e5f5; padding: 0.5rem 1rem; border-radius: 15px; margin-bottom: 0.5rem; text-align: right;">
                    <b>دستیار:</b> {msg['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # ورودی متن کاربر
    user_input = st.chat_input("پیام خود را بنویسید...")
    
    if user_input:
        # اضافه کردن به تاریخچه
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # نمایش پیام کاربر بلافاصله
        with chat_container:
            st.markdown(f"""
            <div style="background-color: #e3f2fd; padding: 0.5rem 1rem; border-radius: 15px; margin-bottom: 0.5rem; text-align: right;">
                <b>شما:</b> {user_input}
            </div>
            """, unsafe_allow_html=True)
        
        # پردازش با دستیار
        with st.spinner("🤔 در حال تفکر..."):
            # مرحله 1: تحلیل واقعیت
            analysis = llm.analyze_reality(user_input, "")
            
            # مرحله 2: تبدیل به بردار
            embedding = embedding_model.encode(user_input)
            
            # مرحله 3: جستجوی مشابه‌ها
            similar = memory.search_similar_realities(
                embedding, 
                user_id=st.session_state.user_id,
                n_results=TOP_K_RESULTS
            )
            
            # مرحله 4: تشخیص تغییر
            is_new = tracker.is_new_reality(analysis, similar)
            
            # مرحله 5: ذخیره در حافظه
            memory.add_reality(st.session_state.user_id, user_input, embedding, analysis)
            
            # مرحله 6: تولید پاسخ
            response = llm.generate_response(user_input, analysis, similar, "")
            
            # ذخیره در تاریخچه واقعیت‌ها
            reality_entry = {
                "timestamp": datetime.now().isoformat(),
                "emotional_state": analysis.get("emotional_state", "نامشخص"),
                "beliefs": ", ".join(analysis.get("beliefs", [])),
                "cognitive_needs": analysis.get("cognitive_needs", ""),
                "is_new_reality": is_new
            }
            st.session_state.reality_history.append(reality_entry)
            
            # اضافه کردن پاسخ به تاریخچه
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            # نمایش پاسخ
            with chat_container:
                st.markdown(f"""
                <div style="background-color: #f3e5f5; padding: 0.5rem 1rem; border-radius: 15px; margin-bottom: 0.5rem; text-align: right;">
                    <b>دستیار:</b> {response}
                </div>
                """, unsafe_allow_html=True)
            
            # نمایش تغییر واقعیت
            if is_new:
                st.toast("✨ واقعیت جدید تشخیص داده شد!", icon="🌟")
        
        # کمی تأخیر برای نمایش بهتر
        time.sleep(0.5)
        st.rerun()


with col2:
    st.subheader("🔍 تحلیل لحظه‌ای واقعیت")
    
    # نمایش آخرین تحلیل (اگر وجود داشته باشد)
    if st.session_state.reality_history:
        last = st.session_state.reality_history[-1]
        
        st.markdown('<div class="reality-box">', unsafe_allow_html=True)
        
        # وضعیت عاطفی با رنگ مناسب
        emotion = last['emotional_state']
        emotion_class = {
            "شاد": "happy",
            "غمگین": "sad",
            "سردرگم": "confused",
            "مشتاق": "curious"
        }.get(emotion, "")
        
        st.markdown(f"""
        <span class="emotion-tag {emotion_class}">😊 {emotion}</span>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**💭 باورها:** {last['beliefs']}")
        st.markdown(f"**🎯 نیاز شناختی:** {last['cognitive_needs']}")
        
        if last.get('is_new_reality', False):
            st.markdown("**✨ وضعیت:** واقعیت جدید ✨")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # نمایش تعداد واقعیت‌های ثبت شده
        st.metric(
            label="📊 تعداد واقعیت‌های ثبت شده",
            value=len(st.session_state.reality_history)
        )
        
        # نمایش مشابه‌های یافت شده
        if similar:
            with st.expander("🔄 واقعیت‌های مشابه قبلی"):
                for i, sim in enumerate(similar[:3]):
                    st.markdown(f"**{i+1}.** {sim['text'][:100]}...")
                    st.caption(f"شباهت: {1 - sim.get('distance', 0):.2f}")
    else:
        st.info("هنوز گفتگویی شروع نشده است. پیامی بفرستید تا تحلیل آغاز شود.")


# ============================================
# نمایش اطلاعات سیستمی در فوتر
# ============================================
st.markdown("---")
with st.expander("ℹ️ اطلاعات فنی"):
    st.markdown(f"""
    - **شناسه کاربر:** {st.session_state.user_id}
    - **تعداد پیام‌ها:** {len(st.session_state.chat_history)}
    - **وضعیت حافظه:** فعال (ChromaDB)
    - **مدل embedding:** {EMBEDDING_MODEL}
    """)