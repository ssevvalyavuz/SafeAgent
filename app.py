import json
import sqlite3
import streamlit as st
from agent import run_security_crew, GatewayDecision
from database import execute_safe_query


#Streamlit sayfa yapılandırması
st.set_page_config(page_title="CrewAI Güvenlik Kontrolü", page_icon="🛡️", layout="centered")

st.title("🛡️ CrewAI Güvenlik Kontrolü")
st.markdown("""
Bu sistem, gelen doğal dil isteklerini analiz eden ve yalnızca güvenlik denetiminden geçen
meşru sorguların veritabanına erişmesine izin veren otonom bir AI Gateway mimarisidir.
""")

st.divider()

# Veritabanı bağlantısını kontrol et
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

#Butonun sola yaslanması için iki sütunlu bir yapı kullanıyoruz.
col1, col2 = st.columns([1, 5])
with col1:
    submit_btn = st.button("Talebi İncele ve Çalıştır", type="primary") 
    
#Projenin asıl karar ve çalıştırma kısmı. Kullanıcıdan gelen promptu alır, güvenlik ekibine gönderir ve sonucu döndürür.

if submit_btn and user_prompt.strip(): #Kullanıcı butona bastı mı, metin kutusuna gerçekten bir şey yazdı mı?
    with st.spinner("CrewAI güvenlik denetimi ve yönlendirme yapılıyor..."):
        # CrewAI ekibini çalıştırıyoruz
        result = run_security_crew(user_prompt)
        
        # Pydantic çıktısını alıyoruz
        try:
            if hasattr(result, "pydantic") and result.pydantic:
                decision: GatewayDecision = result.pydantic
            else:
                decision = result
            
            # İngilizce gelen status değerini arayüz için Türkçeye çeviriyoruz
            durum = "ONAYLANDI" if decision.status == "APPROVED" else "REDDEDİLDİ"
            target_intent = decision.intent
            gerekce = decision.reason
            raw_output = str(decision.model_dump())
        except Exception as e:
            durum = "REDDEDİLDİ"
            target_intent = "none"
            gerekce = f"Şema Doğrulama Hatası: {str(e)}"
            raw_output = str(result)        
            
        st.subheader("🔍 Güvenlik Denetim Raporu")
        st.markdown(f"**DURUM:** {durum}")
        st.markdown(f"**SEÇİLEN INTENT:** `{target_intent}`")
        st.markdown(f"**GEREKÇE:** {gerekce}")
        
        # --- GELİŞTİRİCİ / DEBUG PANELİ ---
        with st.expander(" Model Çıktısını ve Debug Bilgilerini İncele"):
            st.markdown("**1. CrewAI Ham Çıktısı (`raw_output`):**")
            st.code(str(raw_output), language="text")
                    
        st.divider()
        st.subheader("📊 Güvenli Sorgu Sonuçları")
        
        durum_temiz = durum.replace("İ", "I").upper()
        is_approved = "ONAY" in durum_temiz and "RED" not in durum_temiz

        if is_approved and target_intent != "none":
            success, query_result = execute_safe_query(target_intent) #Sorgu başarıyla çalıştı mı (success: True/False) ve veritabanından dönen tablo verisi nedir (query_result) sorularının sonucunu alır; böylece Streamlit arayüzünde kullanıcıya yeşil kutu ve tablo olarak gösterilir.
            if success and query_result is not None:
                st.dataframe(query_result)
            else:
                st.warning("⚠️ Sorgu yürütülemedi veya sonuç bulunamadı.")
        else:
            st.error("⛔ Erişim Reddedildi: İstek güvenlik standartlarını karşılamadığı için veritabanı kilitlendi.")
            st.info("🔒 Zero-Trust İlkesi: Veritabanı bütünlüğü ve PII güvenliği korunmuştur.")