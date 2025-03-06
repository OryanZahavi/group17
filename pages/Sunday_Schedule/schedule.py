# import schedule
# import time
# from db_functions import update_sunday_classes  # מייבאים את פונקציית העדכון
#
# # קביעת תזמון לעדכון ימי ראשון
# schedule.every().thursday.at("22:00").do(update_sunday_classes)
#
# print("🔄 מתזמן פעיל! עדכון ימי ראשון יתבצע כל יום חמישי ב-22:00.")
#
# # לולאה שרצה כל דקה ובודקת אם הגיע הזמן להריץ את הפונקציה
# while True:
#     schedule.run_pending()
#     time.sleep(60)
