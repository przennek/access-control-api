import logging
from typing import Optional

from flask import Blueprint, request, jsonify

from aca.api.db.dto.enrollment_dto import EnrollmentDTO
from aca.api.db.model.enrollment import Enrollment
from aca.common.di import iocc
from aca.common.schema import validate_json_schema, enrollment_json_schema

enrollment_api_bp = Blueprint('enrollment_api', __name__, url_prefix='/api/enrollment')

logger = logging.getLogger(__name__)


@enrollment_api_bp.route("/create", methods=['POST'], endpoint="create_enrollment")
@validate_json_schema(enrollment_json_schema)
def create_enrollment():
    enrollment_json = request.get_json()
    iocc(EnrollmentDTO).create(Enrollment(enrollment_json["code"], enrollment_json["room"]))
    return '', 201


@enrollment_api_bp.route("/get", methods=['GET'], endpoint="get_enrollment")
def get_enrollment():
    code = request.args.get('code')
    enrollment: Optional[Enrollment] = iocc(EnrollmentDTO).find(code)

    if enrollment is not None:
        return jsonify(enrollment.as_dict()), 200

    return '', 404
