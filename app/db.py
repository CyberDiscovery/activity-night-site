from firebase_admin import db

game_suggestions = db.reference("suggestions")
user_db = db.reference("users")


def get_user_record(uid):
    return user_db.get(str(uid))