from crewai import Agent, Task, Crew, Process, LLM

# CrewAI'ın kendi yerleşik LLM sınıfı (LangChain'e gerek yok)
local_llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)

#----AGENTLARIN TANIMLANMASI---

#AGENT 1: Güvenlik Analisti
#Görevi : Girdileri kurumsal risk ve veri açısından otonom analiz eden agent.

#Siber güvenlik uzmanı
security_analyst = Agent(
    role="Kurumsal Güvenlik Analisti",
    goal="Gelen istekleri kurumsal siber güvenlik, veri gizliliği ve sızıntı politikalarına göre analiz etmek.",
    backstory="Finans ve teknoloji alanında uzman kıdemli güvenlik analistisin. İsteklerdeki hassas veri sızıntısı ve saldırı risklerini tespit edersin.",    
    verbose=False,          # Arka planda ajanın ne düşündüğünü terminalde canlı görmek için
    llm=local_llm,          # Lokal Llama 3.2 modelini atıyoruz
    max_iter=1             # M1 Mac'imizi korumak için sonsuz döngü freni! En fazla 3 deneme yapabilir.
)

#AGENT 2: Kod ve İşlem Denetçisi
# Görevi: Analistin raporunu alıp, arka plandaki sisteme/veritabanına zarar gelmeyeceğini onaylamak.

#Sistem veya veritabanı denetleyicisi
operation_auditor = Agent(
    role="Sistem ve İşlem Denetçisi",
    goal="Güvenlik analizinden geçen isteklerin veri tabanına veya sisteme doğrudan zarar vermeyeceğinden emin olmak.",
    backstory="Veritabanı ve sistem güvenliği uzmanısın. Güvenlik raporuna bakarak işlemi kesin olarak ONAYLANDI veya REDDEDİLDİ şeklinde sonuçlandırırsın.",    verbose=False,
    llm=local_llm,
    max_iter=1
)

#----GÖREVLERİN TANIMLANMASI----
#Bu fonksiyonu bir iş akışı gibi düşünebiliriz.
#pipeline
#Kullanıcıdan gelen mesaj bu pipelinea girer.

def run_security_crew(user_prompt):
    """
    Dışarıdan gelen kullanıcı promptunu alır, ajanlara sırayla işletir.
    ve nihai bir 'ONAYLANDI' veya 'REDDEDİLDİ' raporu döner.
    
    """
    #Görev 1: Güvenlik Analizi
    task_security_check = Task(
        description=(
            f"Kullanıcının isteğini analiz et: '{user_prompt}'. "
            "Kural 1: Şirket içi etkinlik takvimi veya herkese açık genel bilgiler düşük risklidir. "
            "Kural 2: SQL kodları, şifreler, özel müşteri verileri veya yetki aşımı yüksek risklidir. "
            "Raporunu sadece Türkçe yaz. Risk puanını 1 ile 10 arasında belirle."
        ),# Task tanımı içinde expected_output'u netleştir:
        expected_output="Maksimum 3 cümlelik kısa bir risk analizi ve 1-10 arası Risk Puanı." ,
        agent=security_analyst
    )
    
    # Görev 2: Teknik Denetim (Analistin çıktısını girdi olarak alacak)

    task_audit_check = Task(
        description=(
            "Güvenlik Analistinin raporuna göre karar ver. "
            "Risk puanı 6 veya üzerindeyse durumu REDDEDİLDİ, 5 ve altındaysa ONAYLANDI olarak belirle. "
            "Cevabını tamamen Türkçe ve şu şablonda yaz:\n"
            "DURUM: [ONAYLANDI / REDDEDİLDİ]\n"
            "GEREKÇE: [Kısa açıklama]"
        ),
        expected_output="Sadece nihai karar metni: 'DURUM: ONAYLANDI' veya 'DURUM: REDDEDİLDİ' ve çok kısa bir teknik gerekçe.",
        agent=operation_auditor,
        context=[task_security_check]  # <-- "Girdi olarak doğrudan Görev 1'in çıktısını al" demek!, crew.ai bunu otomatik olarak yapacak. Task nesnesi, önceki taskın çıktısını alacak şekilde ayarlanabilir.

    ) 
    
    #----EKİBİN KURULMASI VE ÇALISTIRILMASI----

    security_crew = Crew(
        agents=[security_analyst, operation_auditor],
        tasks=[task_security_check, task_audit_check],  
        process=Process.sequential #tasks nesnesine görevleri hangi sırayla yazdıysam o şekilde çalış.
    )

    result = security_crew.kickoff() #tüm sistemi harekete geçir. Agentları uyandır.
    
    return result


    

    
    