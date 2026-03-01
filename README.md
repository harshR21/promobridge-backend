# 🚀 PROMOBRIDGE BACKEND - SETUP KAISE KARE

## ✅ YEH 7 FILES HAIN IS FOLDER MEIN:

1. **main.py** - Main backend application
2. **models.py** - Database models
3. **auth.py** - Authentication system
4. **database.py** - Database connection
5. **requirements.txt** - Python packages list
6. **env-template.txt** - Environment variables template
7. **README.md** - Yeh file (setup guide)

---

## 🎯 SETUP STEPS (10 Minutes)

### STEP 1: Folder Banao
```
1. File Explorer open karo
2. Jaha chahiye folder banao (G:\ ya C:\ ya Desktop)
3. Naam: MyProject
4. Andar ek aur folder: backend
```

### STEP 2: Files Copy Karo
```
Sab 7 files ko backend folder mein copy-paste karo
```

### STEP 3: Command Prompt Kholo
```
1. backend folder mein jao (File Explorer mein)
2. Address bar click karo
3. "cmd" type karo
4. Enter dabao
```

### STEP 4: Check Files
```bash
dir
```
Sab 7 files dikhni chahiye!

### STEP 5: Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```
Success: (venv) dikna chahiye

### STEP 6: Install Packages
```bash
pip install -r requirements.txt
```
Wait 3-5 minutes

### STEP 7: .env File Setup
```bash
copy env-template.txt .env
notepad .env
```
DATABASE_URL edit karo (Supabase connection string)
Save & Close

### STEP 8: Run Backend
```bash
python main.py
```

### STEP 9: Test
Browser: http://localhost:8000/docs

---

## ✅ SUCCESS!

Agar API docs dikhe toh BACKEND READY! 🎉

---

## 📞 HELP

Problem? Batao:
- Kaunse step pe stuck ho?
- Kya error aa rahi hai?

Main help karunga! 💪
