# DreamActor App

אפליקציית ווב המאפשרת להחיות תמונות סטטיות באמצעות קובצי אודיו, תוך שימוש במודל DreamActor-M1.

## התקנה

1. התקן את Python 3.8 ומעלה
2. שכפל את המאגר:
```bash
git clone https://github.com/yourusername/dreamactor-app.git
cd dreamactor-app
```

3. צור סביבה וירטואלית והפעל אותה:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

4. התקן את התלויות:
```bash
pip install -r requirements.txt
```

5. הורד את המודל המאומן:
- הורד את קובץ `model.pth` מ-[DreamTalk Releases](https://github.com/OpenTalker/DreamTalk/releases)
- צור תיקיית `models/DreamActor_M1/checkpoints`
- העתק את `model.pth` לתיקיית `checkpoints`

## הפעלה

1. הפעל את השרת:
```bash
python app.py
```

2. פתח את הדפדפן בכתובת `http://localhost:5000`

3. העלה תמונה וקובץ אודיו:
- בחר תמונה ברורה של פנים
- בחר קובץ אודיו באיכות טובה
- לחץ על "צור אנימציה"

4. המתן לעיבוד והורדת הוידאו המונפש

## דרישות מערכת

- Python 3.8+
- CUDA (אופציונלי, לביצועים משופרים)
- 8GB RAM לפחות
- מעבד חזק (מומלץ Intel i5/i7 או AMD Ryzen 5/7)

## רישיון

MIT License 