import sqlite3

def init_mock_database():
    """
    Şirketin operasyonel, müşteri ve finansal verilerini içeren
    gerçekçi SQLite veritabanını oluşturur ve zengin mock veriler basar.
    """
    conn = sqlite3.connect("company_vault.db")
    cursor = conn.cursor()

    # 1. Tablo: Kullanıcılar ve Roller (RBAC)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            full_name TEXT NOT NULL,
            department TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # 2. Tablo: Müşteri Bilgileri (Hassas Kişisel Veriler - PII)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_code TEXT UNIQUE,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            account_balance REAL NOT NULL
        )
    """)

    # 3. Tablo: Finans ve Şirket Sırları
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS finance_records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            period TEXT NOT NULL,
            department TEXT NOT NULL,
            allocated_budget REAL NOT NULL,
            spent_budget REAL NOT NULL,
            confidential_note TEXT
        )
    """)

    # 4. Tablo: Güvenlik Denetim Günlüğü (Audit Logs - Gateway Logları İçin)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            requested_prompt TEXT NOT NULL,
            risk_score INTEGER,
            decision TEXT NOT NULL,
            decision_reason TEXT
        )
    """)

    # Tabloları temizle
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM customers")
    cursor.execute("DELETE FROM finance_records")

    # Zengin Kullanıcı Listesi
    users_data = [
        ("ahmet_admin", "Ahmet Kaya", "IT & Security", "Admin"),
        ("zeynep_dev", "Zeynep Arda", "Software Engineering", "Senior Developer"),
        ("can_intern", "Can Demir", "Software Engineering", "Intern"),
        ("selin_hr", "Selin Çelik", "Human Resources", "HR Specialist"),
        ("burak_finance", "Burak Yılmaz", "Finance", "Finance Manager"),
        ("elif_marketing", "Elif Şahin", "Marketing", "Content Lead")
    ]
    cursor.executemany("INSERT INTO users (username, full_name, department, role) VALUES (?, ?, ?, ?)", users_data)

    # Zengin Müşteri Listesi (PII)
    customers_data = [
        ("CUST-101", "Mehmet Öztürk", "mehmet.ozturk@email.com", "+905551112233", 145000.0),
        ("CUST-102", "Ayşe Yılmaz", "ayse.yilmaz@email.com", "+905554445566", 28000.5),
        ("CUST-103", "Kemal Sunal", "kemal.sunal@email.com", "+905552223344", 512000.0),
        ("CUST-104", "Fatma Demir", "fatma.demir@email.com", "+905558889900", 12500.0),
        ("CUST-105", "Emre Aydın", "emre.aydin@email.com", "+905556667788", 89400.0),
        ("CUST-106", "Deniz Koç", "deniz.koc@email.com", "+905553334455", 340000.0)
    ]
    cursor.executemany("INSERT INTO customers (customer_code, full_name, email, phone, account_balance) VALUES (?, ?, ?, ?, ?)", customers_data)

    # Zengin Finans Verileri
    finance_data = [
        ("2026-Q1", "Marketing", 350000.0, 310000.0, "Bahar lansmanı kampanyası tamamlandı."),
        ("2026-Q1", "R&D", 1200000.0, 1150000.0, "Otonom yapay zeka ajanları altyapı yatırımı."),
        ("2026-Q2", "Sales", 450000.0, 420000.0, "Yeni CRM entegrasyonu lisanslama bedeli."),
        ("2026-Q2", "Executive Board", 2500000.0, 1800000.0, "Rakip girişimin %15 hisse alım müzakeresi devam ediyor."),
        ("2026-Q3", "IT Operations", 600000.0, 580000.0, "Veri merkezi siber savunma kalkanı güncellendi.")
    ]
    cursor.executemany("INSERT INTO finance_records (period, department, allocated_budget, spent_budget, confidential_note) VALUES (?, ?, ?, ?, ?)", finance_data)

    conn.commit()
    conn.close()
    print("✓ Kurumsal 'company_vault.db' zengin mock veriler ve audit tablosuyla güncellendi!")

if __name__ == "__main__":
    init_mock_database()