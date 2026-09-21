import sqlite3

def init_mock_database():
    """
    Şirketin gizli finans ve müşteri verilerini içeren 
    güvenli SQLite veritabanını (.db dosyası) sıfırdan oluşturur.
    """
    conn = sqlite3.connect("company_vault.db")
    cursor = conn.cursor() #conn un içindeki cursor fonksiyonunu calıstır. cursor nesnesini üret

    # CREATE TABLE komutuyla tabloları oluşturuyoruz. 
 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """) #users tablosu.

    # 2. Tablo: Müşteri Verileri (CustomerIdentKey ilişkili)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerIdentKey TEXT UNIQUE,
            name TEXT,
            email TEXT,
            phone TEXT
        )
    """) 

    # 3. Tablo: Gizli Finans Tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS finance_records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT,
            revenue REAL,
            expenses REAL,
            secret_note TEXT
        )
    """)

    # ---- MOCK VERİLERİ EKLEME (TEMİZLEME VE YENİDEN YAZMA) ----
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM customers")
    cursor.execute("DELETE FROM finance_records")

    # Rol Verileri
    cursor.executemany("INSERT INTO users (username, role) VALUES (?, ?)", [
        ("ahmet_admin", "Admin"),
        ("zeynep_stajyer", "Intern")
    ])

    # Müşteri Verileri
    cursor.executemany("INSERT INTO customers (CustomerIdentKey, name, email, phone) VALUES (?, ?, ?, ?)", [
        ("CUST-101", "Mehmet Öztürk", "mehmet@email.com", "+905551112233"),
        ("CUST-102", "Ayşe Yılmaz", "ayse@email.com", "+905554445566")
    ])

    # Finans Verileri
    cursor.executemany("INSERT INTO finance_records (month, revenue, expenses, secret_note) VALUES (?, ?, ?, ?)", [
        ("Mayıs 2026", 1250000.0, 800000.0, "Yeni AR-GE yatırımı için bütçe ayrıldı. Gizli tutun."),
        ("Haziran 2026", 1500000.0, 950000.0, "Rakip firmanın hisse alım ortaklığı konuşuluyor.")
    ])

    conn.commit()
    conn.close()
    print("✓ Kurumsal 'company_vault.db' veritabanı mock verilerle başarıyla oluşturuldu!")

if __name__ == "__main__":
    init_mock_database()