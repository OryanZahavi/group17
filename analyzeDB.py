from pymongo import MongoClient
import os
from dotenv import load_dotenv


def fetch_collections():
    load_dotenv()

    # קבלת ה-URI של MongoDB ממשתני סביבה
    uri = os.environ.get('DB_URI')
    if not uri:
        print("⚠️ שגיאה: לא נמצא DB_URI בקובץ הסביבה.")
        return

    # התחברות למסד הנתונים
    client = MongoClient(uri)
    db = client["studio_db"]  # שנה לשם המסד שלך

    # שליפת כל האוספים
    collections = db.list_collection_names()

    if collections:
        print("✅ האוספים הקיימים במסד הנתונים studio_db:")
        for collection_name in collections:
            collection = db[collection_name]
            documents = list(collection.find())  # קבלת כל המסמכים

            print(f"📂 אוסף: {collection_name}")

            if documents:
                for doc in documents:
                    print(doc)  # הצגת כל מסמך
            else:
                print("   (אין נתונים באוסף הזה)")

            print("-" * 50)  # מפריד לנוחות קריאה
    else:
        print("⚠️ לא נמצאו אוספים במסד הנתונים studio_db.")


if __name__ == "__main__":
    fetch_collections()
