import os

from flask import Flask, jsonify, make_response, request, abort
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy import exc

from .constants import DATE_FORMAT
from .models import db, User, Vm


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY=os.environ.get("SECRET_KEY", default="dev"))

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)
    Migrate(app, db)

    @app.errorhandler(400)
    def invalid_client_input(error):
        return make_response(jsonify({"error": str(error)}), 400)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({"error": "Not found."}), 404)

    @app.route("/")
    def index():
        return "API is working. Last updated " + app.config.get("APP_VERSION", "0.1")

    # Health check
    @app.route("/healthy")
    def healthy():
        db.engine.execute("SELECT 1")

        return "API is healthy"

    # User Endpoints

    @app.route("/api/users", methods=["GET"])
    def get_users():
        users = list(map(lambda user: user.to_dict(), User.query.all()))
        return jsonify({"users": users}), 200

    @app.route("/api/users/<username>", methods=["GET"])
    def get_user(username):
        user = User.query.filter_by(username=username).first_or_404()
        return jsonify({"user": user.to_dict()}), 200

    @app.route("/api/users", methods=["POST"])
    def create_user():
        payload = request.get_json()

        if "email" not in payload or "username" not in payload:
            abort(
                400,
                """Missed required arguments.
                Email and username must be supplied.""",
            )

        user = User(email=payload["email"], username=payload["username"])
        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            abort(400, "Such email or username already exist.")

        return jsonify({"user": user.to_dict()}), 201

    @app.route("/api/users/<username>", methods=["PUT", "PATCH"])
    def update_user(username):
        payload = request.get_json()
        user = User.query.filter_by(username=username).first_or_404()

        new_email = payload.get("email", user.email)
        new_username = payload.get("username", user.username)
        user.email = new_email
        user.username = new_username

        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            abort(400, "Such email or username already exist.")

        return jsonify({"user": user.to_dict()}), 200

    @app.route("/api/users/<username>", methods=["DELETE"])
    def delete_user(username):
        user = User.query.filter_by(username=username).first_or_404()
        db.session.delete(user)
        db.session.commit()
        return jsonify({"user": user.to_dict()}), 200

    # VM Endpoints

    @app.route("/api/vms", methods=["GET"])
    def get_vms():
        vms = list(map(lambda vm: vm.to_dict(), Vm.query.all()))
        return jsonify({"vms": vms}), 200

    @app.route("/api/vms/<vm_id>", methods=["GET"])
    def get_vm(vm_id):
        vm = Vm.query.filter_by(id=vm_id).first_or_404()
        return jsonify({"vm": vm.to_dict()}), 200

    @app.route("/api/vms", methods=["POST"])
    def create_vm():
        payload = request.get_json()

        if "name" not in payload or "ip" not in payload or "user_id" not in payload:
            abort(
                400,
                """Missed required arguments.
                 Name, ip and user_id must be supplied.""",
            )

        vm_name = payload["name"]
        vm_ip = payload["ip"]
        vm_description = payload.get("description", "")
        vm_status = payload.get("status", "running")

        str_reservation_start = payload.get("reservation_start")
        str_reservation_end = payload.get("reservation_end")

        try:
            vm_reservation_start = None
            vm_reservation_end = None
            if str_reservation_start:
                vm_reservation_start = datetime.strptime(
                    str_reservation_start, DATE_FORMAT
                )
            if str_reservation_end:
                vm_reservation_end = datetime.strptime(str_reservation_end, DATE_FORMAT)
        except ValueError:
            abort(
                400,
                """Invalid datetime format.
                 Please provide data in the `dd/mm/yyyy` format.""",
            )

        vm_user_id = payload["user_id"]

        vm = Vm(
            name=vm_name,
            ip=vm_ip,
            description=vm_description,
            status=vm_status,
            reservation_start=vm_reservation_start,
            reservation_end=vm_reservation_end,
            user_id=vm_user_id,
        )

        try:
            db.session.add(vm)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            abort(400, "Invalid user id.")

        return jsonify({"vm": vm.to_dict()}), 201

    @app.route("/api/vms/<vm_id>", methods=["PUT", "PATCH"])
    def update_vm(vm_id):
        vm = Vm.query.filter_by(id=vm_id).first_or_404()
        payload = request.get_json()

        vm_name = payload.get("name", vm.name)
        vm_description = payload.get("description", vm.description)
        vm_status = payload.get("status", vm.status)

        vm.name = vm_name
        vm.description = vm_description
        vm.status = vm_status

        db.session.add(vm)
        db.session.commit()

        return jsonify({"vm": vm.to_dict()}), 200

    @app.route("/api/vms/<vm_id>", methods=["DELETE"])
    def delete_vm(vm_id):
        vm = Vm.query.filter_by(id=vm_id).first_or_404()
        db.session.delete(vm)
        db.session.commit()
        return jsonify({"vm": vm.to_dict()}), 200

    @app.route("/api/users/<username>/vm-use", methods=["GET"])
    def get_vm_use(username):
        user = User.query.filter_by(username=username).first_or_404()

        return (
            jsonify(
                {
                    "user": user.to_dict(
                        only=("username", "email", "vms", "-vms.user_id")
                    )
                }
            ),
            200,
        )

    return app


def main():
    app = create_app()
    app.run()


if __name__ == "__main__":
    main()
