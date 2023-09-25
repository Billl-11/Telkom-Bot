# Bot Asisten Telkom menggunakan GPT-3.5 LLM

## Deskripsi Proyek
Proyek ini bertujuan untuk membuat bot asisten yang memanfaatkan model bahasa besar GPT-3.5 (Large Language Model) untuk memberikan informasi seputar Telkom dengan dasar data dari situs telkom.co.id. Bot ini akan di-deploy sebagai REST API dengan kemampuan untuk menyimpan percakapan pengguna dan bot ke dalam database MySQL.

##  Langkah-langkah Implementasi
Berikut adalah langkah-langkah implementasi proyek ini:

**1. Pemahaman GPT-3.5 LLM:**
Proyek ini menggunakan LLM GPT-3.5-turbo yang diakses melalui API OpenAI.

**2. Integrasi dengan Data Telkom.co.id:**
Web scraping dari situs web telkom.co.id menggunakan library web scraping BeautifulSoup.

**3. Pengembangan Bot Asisten:**
Library LangChain digunakan untuk membuat LLM asisten yang dapat menjawab pertanyaan pengguna berdasarkan data yang diambil dari telkom.co.id.

**4. Deployment sebagai REST API:**
Deploy bot asisten sebagai REST API menggunakan framework Flask.

**5. Database MySQL:**
Database MySQL digunakan untuk menyimpan percakapan pengguna dan bot.

**6. Parameter topic_id:**
API memiliki parameter topic_id yang digunakan untuk mengidentifikasi percakapan pengguna dan bot. Parameter ini juga berfungsi agar pengguna dapat melanjutkan percakapan terdahulu

## Penggunaan API