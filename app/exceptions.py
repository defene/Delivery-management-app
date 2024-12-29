import logging
from flask import jsonify, current_app

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """输入验证错误"""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class DatabaseError(Exception):
    """数据库错误"""
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        
class AuthenticationError(Exception):
    """认证错误"""
    def __init__(self, message="Authentication failed"):
        super().__init__(message)
        self.message = message

class PermissionError(Exception):
    """权限错误"""
    def __init__(self, message="Permission denied"):
        super().__init__(message)
        self.message = message

class UnexpectedError(Exception):
    """未捕获的异常"""
    def __init__(self, message="An unexpected error occurred"):
        super().__init__(message)
        self.message = message

class TokenError(Exception):
    """For invalid or expired token issues."""
    pass

# 统一异常处理函数
def handle_exception(e):
    """
    统一异常处理
    """
    if isinstance(e, ValidationError):
        logger.warning(f"Validation error: {e.message}")
        return jsonify({"error": e.message}), 400

    elif isinstance(e, DatabaseError):
        logger.error(f"Database error: {e.message}")
        return jsonify({"error": "Database error occurred"}), 500

    elif isinstance(e, AuthenticationError):
        logger.warning(f"Authentication error: {e.message}")
        return jsonify({"error": e.message}), 401

    elif isinstance(e, PermissionError):
        logger.warning(f"Permission error: {e.message}")
        return jsonify({"error": e.message}), 403

    elif isinstance(e, UnexpectedError):
        logger.error(f"Unexpected error: {e.message}")
        return jsonify({"error": e.message}), 500

    else:
        # 处理未捕获的异常
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        
        # 返回详细调试信息（仅在开发环境中）
        if current_app.config.get("DEBUG", False):
            return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
        return jsonify({"error": "An unexpected error occurred"}), 500
