from crewai import Agent, Task, Crew, Process, LLM

# CrewAI'ın kendi yerleşik LLM sınıfı (LangChain'e gerek yok)
local_llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434",
    temperature=0.1,
    num_ctx=2048  # Varsayılan 8k yerine 2048'e düşürmek hızı belirgin artırır
)

#----AGENTLARIN TANIMLANMASI---

#AGENT 1: Güvenlik Analisti
#Görevi : Girdileri kurumsal risk ve veri açısından otonom analiz eden agent.

#Siber güvenlik uzmanı
security_analyst = Agent(
    role="Kurumsal Güvenlik Analisti",
    goal="Gelen istekleri kurumsal siber güvenlik, veri gizliliği ve sızıntı politikalarına göre analiz etmek.",
    backstory="""Sen bir finans ve teknoloji şirketinde 10 yıllık deneyime sahip baş siber güvenlik analistisin. 
    Görevin, guardrail katmanından geçen ancak içerik olarak şirket politikalarını çiğneyebilecek (örneğin müşteri verilerini dışarı sızdırmaya çalışan veya gizli iş mantıklarını öğrenmeye çalışan) istekleri tespit etmektir.""",
    verbose=False,          # Arka planda ajanın ne düşündüğünü terminalde canlı görmek için
    llm=local_llm,          # Lokal Llama 3.2 modelini atıyoruz
    max_iter=3             # M1 Mac'imizi korumak için sonsuz döngü freni! En fazla 3 deneme yapabilir.
)

#AGENT 2: Kod ve İşlem Denetçisi
# Görevi: Analistin raporunu alıp, arka plandaki sisteme/veritabanına zarar gelmeyeceğini onaylamak.

#Sistem veya veritabanı denetleyicisi
operation_auditor = Agent(
    role="Sistem ve İşlem Denetçisi",
    goal="Güvenlik analizinden geçen isteklerin veri tabanına veya sisteme doğrudan zarar vermeyeceğinden emin olmak.",
    backstory="""Sen veri tabanı mimarileri ve güvenli sistem operasyonları konusunda uzman bir mühendissin. 
    Güvenlik Analistinin hazırladığı raporu okur, kullanıcının yapmak istediği işlemin (örneğin veri tabanından veri çekme isteği) arka plandaki sisteme teknik bir zarar (SQL kilitlenmesi, yetkisiz erişim vb.) vermeyeceğinden emin olursun.""",
    verbose=False,
    llm=local_llm,
    max_iter=3
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
    s
    #Görev 1: Güvenlik Analizi
    task_security_check = Task(
        description=f"Şu kullanıcı isteğini kurumsal siber güvenlik kurallarına göre incele: '{user_prompt}'...",
# Task tanımı içinde expected_output'u netleştir:
        expected_output="Maksimum 3 cümlelik kısa bir risk analizi ve 1-10 arası Risk Puanı." ,
        agent=security_analyst
    )
    
    # Görev 2: Teknik Denetim (Analistin çıktısını girdi olarak alacak)

    task_audit_check = Task(
        description="Güvenlik Analistinin hazırladığı raporu incele. Eğer analist ciddi bir risk bulduysa işlemi doğrudan 'REDDEDİLDİ' olarak işaretle. Risk yoksa ve teknik olarak güvenliyse işlemi 'ONAYLANDI' olarak raporla.",
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


    

    
    