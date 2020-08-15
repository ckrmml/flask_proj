from app import create_app, db, cli
from app.database import init_db
from app.database.models import User


app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
    return {'db': db}

@app.before_first_request
def create_user():
    init_db()
    user = User.query.filter_by(name='chris').first()
    if user is None:
        user = User(name='chris', mail="test@me.com")
        user.set_password('test')
        user.confirmed = True
        user.active = True
        db.add(user)
        db.commit()
