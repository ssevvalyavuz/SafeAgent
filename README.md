# 🛡️ SafeAgent: AI Destekli Güvenlik Ağ Geçidi

SafeAgent, kullanıcı komutlarını ve sorgularını LLM tabanlı bir denetim sürecinden geçirerek yetkisiz veri erişimini ve zararlı veritabanı işlemlerini engelleyen çoklu ajanlı (Multi-Agent) bir güvenlik katmanıdır.

## 🚀 Temel Özellikler
- **Çoklu Ajan Denetimi:** CrewAI tabanlı iki bağımsız ajan (Güvenlik Analisti ve Sistem Denetçisi) ile istek doğrulama.
- **Yerel LLM:** Ollama üzerinden çalışan Llama 3.2 modeli ile şirket verilerini dışarıya çıkarmadan yerel çıkarım.
- **Görsel Arayüz:** Streamlit tabanlı interaktif test ve denetim paneli.
- **Güvenlik Politikaları:** Rol yetkileri, hassas veri sızıntı koruması ve SQL injection kontrolü.

## 🛠️ Teknoloji Yığını
- **Dil:** Python 3.10+
- **Ajan Çatısı:** CrewAI
- **Arayüz:** Streamlit
- **Yerel Model:** Ollama (Llama 3.2)
- **Veritabanı:** SQLite (`company_vault.db`)

## ⚙️ Kurulum ve Çalıştırma

1. **Depoyu Klonlayın:**
   ```bash
   git clone [https://github.com/ssevvalyavuz/SafeAgent.git](https://github.com/ssevvalyavuz/SafeAgent.git)
   cd SafeAgent
   ```

2. **Sanal Ortamı Kurun ve Etkinleştirin:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Ollama Modelini Başlatın:**
   ```bash
   ollama run llama3.2
   ```

4. **Arayüzü Çalıştırın:**
   ```bash
   streamlit run app.py
   ```