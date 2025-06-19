# 🔍 Code Analyzer FastAPI

מערכת מבוססת FastAPI המאפשרת ניתוח קוד סטטי של קבצי תכנות (Python, JavaScript, TypeScript, Java, ועוד) ומציגה אזהרות גרפיות וטקסטואליות בנוגע לבעיות נפוצות בקוד.

---

## 🚀 סקירה כללית

פרויקט זה מספק שירותי ניתוח סטטי לקבצי קוד שמועלים לשרת, ובודק עבורם:

- פונקציות ארוכות מדי
- קבצים עם יותר מדי שורות
- משתנים שלא נעשה בהם שימוש
- פונקציות ללא docstring

בנוסף, המערכת יוצרת גרפים סטטיסטיים להצגת נתוני האזהרות:

- היסטוגרמת אורכי פונקציות
- גרף עוגה לפי סוגי הבעיות
- גרף עמודות המשווה את מספר הבעיות בין קבצים

---

## ⚙️ הוראות התקנה וביצוע

1. **העתקת הפרויקט**:
   ```bash
   git clone <repository-url>
   cd <project-folder>
   ```

2. **התקנת סביבת עבודה** (מומלץ):
   ```bash
   python -m venv venv
   source venv/bin/activate        # ב-Windows: venv\Scripts\activate
   ```

3. **התקנת התלויות**:
   ```bash
   pip install fastapi uvicorn matplotlib
   ```

4. **הרצת השרת**:
   ```bash
   uvicorn main:app --reload
   ```

5. **בדיקת המערכת**:
   פתח דפדפן וגש לכתובת:
   ```
   http://localhost:8000/docs
   ```

---

## 📁 מבנה תיקיות

```
project/
│
├── main.py              # קובץ FastAPI הראשי עם הנתיבים /alerts ו-/analyze
├── analyze.py           # פונקציות ליצירת גרפים והפקת אורכי פונקציות
├── alerts.py            # פונקציות לזיהוי בעיות בקוד (אורך פונקציות, משתנים וכו')
├── graphs/              # תיקייה לאחסון גרפים PNG שנוצרים
│   └── *.png
├── README.md            # קובץ תיעוד זה
└── requirements.txt     # רשימת תלויות (לא חובה, ראה הערה למטה)
```

---

## 🔌 הסבר על נקודות הקצה (Endpoints)

### 📍 POST `/alerts`

מבצע ניתוח טקסטואלי של קבצים ומחזיר רשימת אזהרות עבור כל קובץ שהועלה.

**קלט**:
- רשימת קבצים (`multipart/form-data`)

**פלט לדוגמה**:
```json
[
  {
    "filename": "example.py",
    "warnings": [
      "Function 'foo' is too long: 31 lines",
      "Variable 'x' is assigned but never used"
    ]
  },
  {
    "filename": "broken.py",
    "error": "unexpected indent"
  }
]
```

---

### 📍 POST `/analyze`

מבצע ניתוח גרפי ומחזיר:
- גרף היסטוגרמה של אורכי פונקציות
- גרף עוגה של סוגי בעיות
- גרף עמודות של סך הבעיות בכל קובץ

**קלט**:
- רשימת קבצים (`multipart/form-data`)

**פלט לדוגמה**:
```json
{
  "files": [
    {
      "filename": "script.py",
      "function_length_graph": "/graphs/abcd1234.png",
      "issues_pie_chart": "/graphs/efgh5678.png"
    }
  ],
  "issues_bar_chart": "/graphs/ijkl9012.png"
}
```

---

## 🛠 דרישות ותלויות

ניתן לרשום את תלויות הפרויקט בקובץ `requirements.txt`:

```txt
fastapi
uvicorn
matplotlib
```

להתקנתן:
```bash
pip install -r requirements.txt
```

---

## 📝 הערות

- הנתונים אינם נשמרים בבסיס נתונים — הכל מתבצע בזיכרון ובקבצים זמניים בתיקיית `graphs`.
- סיומות קבצים נתמכות: `.py`, `.java`, `.js`, `.ts`, `.cpp`, `.c`
- הקוד מתמקד בניתוח קבצי **Python** בשלב זה, אך יש לו התאמה חלקית לשפות אחרות לצורך סינון בסיסי.
- כל גרף נוצר בקובץ `PNG` חדש עם שם ייחודי ומונגש דרך נתיב `/graphs/<filename>`.

---

## 📧 יצירת קשר

לשאלות או בעיות ניתן ליצור קשר עם מפתח/ת המערכת.

---

בהצלחה! 🚀