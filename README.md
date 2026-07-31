# 💰 Kirim-Chiqim (Income & Expense Tracker) Backend REST API

> **8-oy imtihon loyihasi (Maksimal 100 ball)**  
> Ushbu loyiha shaxsiy va korporativ moliyaviy kirim hamda chiqimlarni nazorat qiluvchi, ko'p tilli (Uzbek, Russian, English), analitik hisobotlar beruvchi va Swagger/Postman hujjatlariga ega to'liq Django REST Framework backend tizimidir.

---

## 🌟 Loyiha Imkoniyatlari va Texnologiyalar

### Texnologik Steck:
- **Backend Framework**: Python 3.13, Django 5.x, Django REST Framework (DRF)
- **Autentifikatsiya**: SimpleJWT (JSON Web Tokens)
- **API Hujjatlashtirish**: Swagger UI & ReDoc (`drf-spectacular`), Postman Collection
- **Ma'lumotlar bazasi**: SQLite3 / PostgreSQL
- **Ko'p tillilik (Multilingual)**: Uzbek (`uz`), Russian (`ru`), English (`en`)
- **Frontend Dashboard**: Interaktiv HTML5, CSS3, JavaScript & Chart.js

---

## 📐 Ma'lumotlar Bazasi Sxemasi (Database Architecture)

```
+------------------+         +------------------+         +----------------------+
|       User       | 1 --- * |     Account      | 1 --- * |     Transaction      |
|------------------|         |------------------|         |----------------------|
| id (PK)          |         | id (PK)          |         | id (PK)              |
| username         |         | user_id (FK)     |         | type (EXPENSE/INCOME)|
| email            |         | name (Naqd, Card)|         | amount               |
| preferred_lang   |         | balance          |         | transaction_date     |
+------------------+         | currency         |         | comment / photo      |
                             +------------------+         | account_id (FK)      |
                                                          | category_id (FK)     |
                                                          +----------------------+
                                                                     |
                                                                     *
                                                          +----------------------+
                                                          |       Category       |
                                                          |----------------------|
                                                          | id (PK)              |
                                                          | name_uz, name_ru...  |
                                                          | type (EXPENSE/INCOME)|
                                                          +----------------------+
```

---

## 🚀 Loyihani Ishga Tushirish (Quick Start)

### 1. Virtual Muhit Yaratish va Aktivlashtirish:
```bash
python -m venv venv
# Windows uchun:
.\venv\Scripts\activate
```

### 2. Kutubxonalarni O'rnatish:
```bash
pip install -r requirements.txt
```

### 3. Database Migratsiyalarini Bajarish:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Boshlang'ich Ma'lumotlar va Adminni Yuklash (Seed Data):
```bash
python manage.py seed_data
```
*Ushbu komanda avtomatik ravishda demo kategoriyalar, `admin` foydalanuvchisi (parol: `admin123`) va namuna hisoblarni yaratadi.*

### 5. Serverni Ishga Tushirish:
```bash
python manage.py runserver
```

---

## 🔗 API Hujjatlari va Interfeyslar

- 📱 **Visual Dashboard (Veb Panel)**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 📄 **Swagger UI Documentation**: [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)
- 📖 **ReDoc Documentation**: [http://127.0.0.1:8000/api/schema/redoc/](http://127.0.0.1:8000/api/schema/redoc/)
- 📮 **Postman Collection**: Loyiha ildizida joylashgan `postman_collection.json` faylini Postman dasturiga import qiling.

---

## 🌐 3 Xil Tilda Ishlash Mexanizmi

API sarlavhalarida (Headers) `Accept-Language: uz`, `ru` yoki `en` qiymatini yuborish orqali javoblarni mos tilda olishingiz mumkin. Shuningdek query parametr orqali ham ishlatsa bo'ladi:
```http
GET /api/v1/categories/?type=EXPENSE&lang=ru
```

---

## 🎓 IMTIHON XIMOYA QILISH QO'LLANMASI (Student Defense Guide)

Imtihonda loyihani himoya qilganda quyidagi kod va mantiqiy savollarga javob berishingiz talab qilinadi:

### 1-Savol: Tranzaksiya (Kirim/Chiqim) bajarilganda hisob balansi qanday o'zgaradi?
> **Javob**: Tranzaksiya saqlanganda (`save()` metodi) va o'chirilganda (`delete()` metodi) `apps/transactions/models.py` dagi `@db_transaction.atomic` dekoratori ostida balans avtomatik qayta hisoblanadi. 
> - **Chiqim (EXPENSE)** yuz berganda `account.balance -= amount` amali bajariladi.
> - **Kirim (INCOME)** yuz berganda `account.balance += amount` amali bajariladi.
> - Tranzaksiya o'chirilsa yoki tahrirlansa eski summa bekor qilinib, yangisi kiritiladi.

### 2-Savol: 3 tilda javob qaytarish kodingizda qayerda amalga oshirilgan?
> **Javob**: `Category` modelida `name_uz`, `name_ru`, `name_en` maydonlari mavjud. `CategorySerializer` serializerining `get_name()` metodida so'rov yuborgan foydalanuvchining `Accept-Language` sarlavhasi yoki `?lang=` parametri o'qib olinib, kerakli dildagi kategoriya nomi qaytariladi.

### 3-Savol: Analitika va hisobotlar (foizlar va summalar) qanday hisoblanmoqda?
> **Javob**: `apps/reports/views.py` dagi `CategoryBreakdownReportView` ko'rinishida Django ORM-ning `aggregate(total=Sum('amount'))` va `values('category').annotate(total=Sum('amount'))` funksiyalaridan foydalanilgan. Jami summadan kelib chiqib, har bir kategoriyaning ulushi foizda (`(total / grand_total) * 100`) hisoblab beriladi.

---
© 2026 Kirim-Chiqim Loyihasi. Barcha huquqlar himoyalangan.
