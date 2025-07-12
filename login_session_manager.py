import asyncio
import os
from twikit import Client
from src.utils.anti_detection import AntiDetectionUtils
from dotenv import load_dotenv

load_dotenv()

SESSION_FILE = 'twitter_session.json'

async def login_and_save_session(username, email, password):
    client = Client('en-US')
    try:
        print("Mencoba login...")
        await AntiDetectionUtils.random_delay(2, 5) # Add random delay before login
        await client.login(auth_info_1=username, auth_info_2=email, password=password)
        await AntiDetectionUtils.random_delay(1, 3) # Add random delay after successful login
        client.save_cookies(SESSION_FILE)
        print(f"✅ Login berhasil dan sesi disimpan ke {SESSION_FILE}")
        return True
    except Exception as e:
        print(f"❌ Gagal login: {e}")
        return False

async def load_session():
    client = Client('en-US')
    if os.path.exists(SESSION_FILE):
        try:
            client.load_cookies(SESSION_FILE)
            print("✅ Sesi berhasil dimuat.")
            return client
        except Exception as e:
            print(f"⚠️ Gagal memuat sesi: {e}. Sesi mungkin kadaluarsa atau rusak.")
            return None
    else:
        print("ℹ️ File sesi tidak ditemukan.")
        return None

async def main():
    print("\n--- Twitter Session Manager ---")
    print("Pilih opsi:")
    print("1. Login dan simpan sesi baru (dari .env atau input manual)")
    print("2. Coba muat sesi yang sudah ada")
    print("-------------------------------")

    choice = input("Masukkan pilihan (1/2): ")

    if choice == '1':
        username = os.getenv('TWITTER_USERNAME')
        email = os.getenv('TWITTER_EMAIL')
        password = os.getenv('TWITTER_PASSWORD')

        if not (username and email and password):
            print("Kredensial tidak ditemukan di .env. Silakan masukkan secara manual.")
            username = input("Masukkan username Twitter: ")
            email = input("Masukkan email Twitter: ")
            password = input("Masukkan password Twitter: ")
        else:
            print("Menggunakan kredensial dari .env...")
            print(f"Username: {username}")
            print(f"Email: {email}")

        await login_and_save_session(username, email, password)
    elif choice == '2':
        client = await load_session()
        if client:
            print("Sesi aktif dan siap digunakan.")
        else:
            print("Tidak dapat memuat sesi. Silakan coba login baru.")
    else:
        print("Pilihan tidak valid.")

if __name__ == '__main__':
    asyncio.run(main())


