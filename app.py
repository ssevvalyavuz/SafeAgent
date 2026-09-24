import json
import sqlite3
import streamlit as st
from agent import run_security_crew
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
        raw_output = run_security_crew(user_prompt) #Arka planda agent.py'deki run_security_crew fonksiyonu çalışıyor ve üç agent sırayla devreye giriyor.
        
        # JSON temizleme ve ayrıştırma
        clean_json_str = str(raw_output).replace("```json", "").replace("```", "").strip()
       
       
       #Yapay zeka modelleri bazen beklenmedik formatta çıktı üretebilir. böyle bir durumda json.loads() patlar ve program 
       #try blogunu terk edip except kısmına duser.
       
        parse_error = None
        try:
            decision_data = json.loads(clean_json_str) #düz yazı halindeki JSON'u Python sözlüğüne çeviriyoruz.
            durum = decision_data.get("durum", "REDDEDİLDİ") #Eğer sözlükte durum anahtarı yoksa varsayılan olarak REDDEDİLDİ kabul ediyoruz.(Zero-Trust ilkesi)
            target_intent = decision_data.get("intent", "none")
            gerekce = decision_data.get("gerekce", "")
        except Exception as e:
            parse_error = str(e)
            # Beklenmedik format veya bozuk JSON durumunda güvenli kilit (Fail-Safe)
            # Niyetten ve onaydan emin olamadığımız için varsayımda bulunmuyoruz, işlemi durduruyoruz.
            durum = "REDDEDİLDİ"
            target_intent = "none"
            gerekce = "Sistem Hatası: Ajan yanıtı geçerli bir formatta ayrıştırılamadı. Güvenlik gereği veritabanı erişimi engellendi."
        st.subheader("🔍 Güvenlik Denetim Raporu")
        st.markdown(f"**DURUM:** {durum}")
        st.markdown(f"**SEÇİLEN INTENT:** `{target_intent}`")
        st.markdown(f"**GEREKÇE:** {gerekce}")
        
        # --- GELİŞTİRİCİ / DEBUG PANELİ ---
        with st.expander(" Model Çıktısını ve Debug Bilgilerini İncele"):
            st.markdown("**1. CrewAI Ham Çıktısı (`raw_output`):**")
            st.code(str(raw_output), language="text")
            
            st.markdown("**2. Temizlenmiş Metin (`clean_json_str`):**")
            st.code(clean_json_str, language="json")
            
            if parse_error:
                st.error(f"Ayrıştırma (JSON Parse) Hatası: {parse_error}")
        
        st.divider()
        st.subheader("📊 Güvenli Sorgu Sonuçları")
        
        if durum == "ONAYLANDI" and target_intent != "none":
            success, query_result = execute_safe_query(target_intent)
            if success and query_result is not None:
                st.dataframe(query_result)
            else:
                st.warning("⚠️ Sorgu yürütülemedi veya sonuç bulunamadı.")
        else:
            st.error("⛔ Erişim Reddedildi: İstek güvenlik standartlarını karşılamadığı için veritabanı kilitlendi.")
            st.info("🔒 Zero-Trust İlkesi: Veritabanı bütünlüğü ve PII güvenliği korunmuştur.")