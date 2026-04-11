from werkzeug.security import generate_password_hash

from flaskr import create_app
from flaskr.core.extensions import db
from flaskr.domains.role.models import Role
from flaskr.domains.user.models import User

config_name = "development"
app = create_app(config_name=config_name)


@app.cli.command("init-db")
def init_db_command():
    with app.app_context():
        from flaskr.core.extensions import db

        db.create_all()

    print("Successfully created tables")


@app.cli.command("seed-db")
def seed_db_command():
    existing_roles = db.session.execute(db.select(Role.name)).scalars().all()

    if "admin" not in existing_roles:
        admin: Role = Role(name="admin")
        db.session.add(admin)

    if "service_staff" not in existing_roles:
        service_staff: Role = Role(name="service_staff")
        db.session.add(service_staff)

    if "kitchen_staff" not in existing_roles:
        kitchen_staff: Role = Role(name="kitchen_staff")
        db.session.add(kitchen_staff)

    try:
        db.session.commit()
        print("Successfully created a roles.")
    except Exception as e:
        db.session.rollback()
        print(e)


@app.cli.command("seed-users")
def seed_user_command():
    existing_users = db.session.execute(db.select(User.username)).scalars().all()
    admin_role = db.session.execute(
        db.select(Role).where(Role.name == "admin")
    ).scalar_one_or_none()

    if not admin_role:
        print("Admin role not found. Run seed-db first.")
        return

    if "admin" not in existing_users:
        admin: User = User(
            username="admin",
            password=generate_password_hash("asdf1234"),
            display_name="Admin",
            email="me@denizugurgenc.com",
            role_id=admin_role.id,
        )
        db.session.add(admin)

    try:
        db.session.commit()
        print("Successfully created a admin user.")
    except Exception as e:
        db.session.rollback()
        print(e)


if __name__ == "__main__":
    app.run()
