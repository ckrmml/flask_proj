from app.database.models.user import User


def is_unique_name(name):
    user = User.query.filter_by(name=name).first()
    if user is None: return True
    return False


def is_unique_mail(mail):
    user = User.query.filter_by(mail=mail).first()
    if user is None: return True
    return False
