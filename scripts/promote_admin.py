import sys, os, argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from app.extensions import db
from app.models import User


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', required=True)
    args = parser.parse_args()
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(username=args.username).first()
        if not user:
            print('User not found')
            return
        user.role = 'admin'
        db.session.commit()
        print('Promoted to admin:', user.username)


if __name__ == '__main__':
    main()