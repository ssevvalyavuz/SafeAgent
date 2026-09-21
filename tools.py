#Agentların python ile düzenli sorgu olusturabilmesi icin SQL sorgulama aracı yazacagız.

import sqlite3
from crewai.tools import tool

@tool ("Sirket kullanici sorma araci")

def check_user_role(username: str) -> str:
    """
    Veritabanına (company_vault.db) bağlanarak, verilen kullanicinin
    sirketteki rolunu sorgular ve doner.

    """
    try:
        conn = sqlite3.connect("company_vault.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result :
            return f"Kullanıcı: {username}, Şirketteki Rolü: {result[0]}"
        else:
            return f"Kullanıcı: {username} veritabanında bulunamadı! Yetkisiz dış kullanıcı olabilir."
    except Exception as e:
            return f"Veritabanı sorgusu sırasında hata oluştu: {str(e)}"