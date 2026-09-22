import sqlite3
import streamlit as st
from agent import run_security_crew
from database import execute_safe_query

st.set_page_config(page_title="CrewAI Güvenlik Kontrolü", page_icon="🛡️", layout="centered")

st.title("🛡️ CrewAI Güvenlik Kontrolü")
st.markdown("""
Bu sistem, gelen doğal dil isteklerini analiz eden ve yalnızca güvenlik denetiminden geçen
meşru sorguların veritabanına erişmesine izin veren otonom bir AI Gateway mimarisidir.
""")

st.divider()

#veritabanı bağlantısını kontrol et
with st.sidebar:
    st.header("⚙️ Sistem Durumu")
    try:
        conn = sqlite3.connect("company_vault.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall() if t[0] != "sqlite_sequence"]
        conn.close()
        
        st.success("🟢 Veritabanı Bağlantısı: Aktif")
        st.caption(f"Mevcut Tablolar: `{', '.join(tables)}`")
    except Exception as e:
        st.error("🔴 Veritabanı Bağlantısı: Başarısız")
        st.caption(f"Hata: {str(e)}")
        
user_prompt = st.text_area("Lütfen sorgunuzu veya isteğinizi girin:", placeholder="Örn: 'Marketing departmanının 2026-Q1 bütçe kullanımını göster.'")

col1, col2 = st.columns([1, 5])
with col1:
    submit_btn = st.button("Talebi İncele ve Çalıştır", type="primary") 
    
if submit_btn and user_prompt.strip():
    with st.spinner("CrewAI güvenlik denetimi ve sorgu yürütülüyor..."):
        result_text = str(run_security_crew(user_prompt))
        st.subheader("🔍 Güvenlik Denetim Raporu")
        st.markdown(result_text)
        
        st.divider()
        st.subheader("📊 Güvenli Sorgu Sonuçları")
        
        #karar metninde "ONAYLANDI" kontrolü
        
        if "DURUM : ONAYLANDI" in result_text or "ONAYLANDI" in result_text.upper():
            prompt_clean = user_prompt.lower().replace("ı", "i").replace("ç", "c").replace("ş", "s")

            if any(w in prompt_clean for w in ["pazarlama", "marketing"]):
                target_intent = "marketing_budget"
            elif any(w in prompt_clean for w in ["calisan", "personel", "rehber", "user", "kullanici", "ekip"]):
                target_intent = "public_directory"
            else:
                target_intent = "general_budget"              
            success, query_result = execute_safe_query(target_intent)
            
            if success:
                # Her şey yolunda, query_result bir tablodur, ekrana bas:
                st.dataframe(query_result)
            else:
                # Bir sorun çıktı, query_result bir hata mesajıdır, kırmızı uyarı bas:
                st.error(f"Sorgu yürütülürken hata oluştu: {query_result}")
        else:
            st.error("⛔ Erişim Reddedildi: İstek güvenlik standartlarını karşılamadığı için veritabanı bağlantısı açılmadı.")
            st.info("🔒 Zero-Trust İlkesi: Veritabanı bütünlüğü ve PII güvenliği korunmuştur.")


       