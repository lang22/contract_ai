from flask import Blueprint, render_template

main_error = Blueprint('main_error', __name__)  # 创建绑定蓝本gen


@main_error.app_errorhandler(404)
def page_not_found(e):
    return render_template('error_404.html'), 404


@main_error.app_errorhandler(500)
def page_error(e):
    return render_template('error_500.html'), 500



