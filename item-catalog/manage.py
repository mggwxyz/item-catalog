# services/users/manage.py

from flask.cli import FlaskGroup

from app import initialize_app

app = initialize_app()
cli = FlaskGroup(create_app=initialize_app)

# @cli.command()
# def recreate_db():
#     db.drop_all()
#     db.create_all()
#     db.session.commit()
#
# @cli.command()
# def seed_db():
#     """Seeds the database."""
#     db.session.add(User(
#         username='michael',
#         email='michael@reallynotreal.com',
#         password='greaterthaneight'
#     ))
#     db.session.add(User(
#         username='michaelherman',
#         email='michael@mherman.org',
#         password='greaterthaneight'
#     ))
#     db.session.commit()




if __name__ == '__main__':
    cli()