from flask import Blueprint, jsonify

import report_service

bp = Blueprint("reports", __name__)


@bp.route("/reports/overdue", methods=["GET"])
def overdue_report():
    return jsonify(report_service.overdue_report())


@bp.route("/reports/summary", methods=["GET"])
def summary_report():
    return jsonify(report_service.summary_report())
