import streamlit as st
from agent import run_security_crew

st.set_page_config(page_title="CrewAI Güvenlik Kontrolü", page_icon="🛡️", layout="centered")

st.title("🛡️ CrewAI Güvenlik Kontrolü")
st.caption("Bu uygulama, kullanıcı isteklerini kurumsal siber güvenlik kurallarına göre analiz eden bir iş akışı simülasyonu sunar.")

user_prompt = st.text_area("Kullanıcı İsteğini Girin:", placeholder="Örn: Şirketin geçen ayki gizli finansal raporlarına erişmek istiyorum, yetkim var.", height=150)

if st.button("İsteği Analiz Et"):
    if user_prompt.strip() == "":
        st.warning("Lütfen bir kullanıcı isteği girin.")
    else:
        with st.spinner("İstek analiz ediliyor..."):
            final_report = run_security_crew(user_prompt)
        
        st.success("Analiz Tamamlandı!")
        st.subheader("Nihai Rapor:")
        st.text_area("Rapor:", value=final_report, height=200, max_chars=None, key="final_report")
        
       