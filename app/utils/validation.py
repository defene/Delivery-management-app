import json
import imghdr
from flask import session
from app.exceptions import ValidationError

class Validator:
    @staticmethod
    def validate_required_fields(data, required_fields):
        """
        验证表单中的必填字段
        """
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing '{field}' field")

    @staticmethod
    def validate_json_field(json_field, field_name):
        """
        验证 JSON 格式字段
        """
        if not json_field:
            return []
        try:
            parsed_data = json.loads(json_field)
            if not isinstance(parsed_data, list):
                raise ValidationError(f"'{field_name}' must be a list")
            return parsed_data
        except json.JSONDecodeError:
            raise ValidationError(f"Invalid JSON format for '{field_name}'")

    @staticmethod
    def validate_file(file, allowed_types=None):
        """
        验证文件是否存在以及类型是否合法
        """
        if not file:
            raise ValidationError("File upload is required")
        file_type = imghdr.what(file)
        if allowed_types and file_type not in allowed_types:
            raise ValidationError(f"Only {', '.join(allowed_types).upper()} files are allowed")
        
    @staticmethod
    def validate_query_params(params, validation_rules):
        """
        验证查询参数
        :param params: 参数字典
        :param validation_rules: 验证规则字典，格式为 {param_name: (required, type)}
        """
        for param, (required, param_type) in validation_rules.items():
            value = params.get(param)
            
            # 检查是否为必填参数
            if required and value is None:
                raise ValidationError(f"'{param}' is required.")
            
            # 检查参数类型
            if value is not None and not isinstance(value, param_type):
                raise ValidationError(f"'{param}' must be of type {param_type.__name__}.")

    @staticmethod
    def validate_positive_int(value, field_name):
        """
        验证正整数参数
        """
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValidationError(f"'{field_name}' must be a positive integer.")
        
    @staticmethod
    def validate_enum(value, valid_values, field_name):
        """
        验证参数是否属于指定枚举值
        """
        if value is not None and value not in valid_values:
            raise ValidationError(f"'{field_name}' must be one of {valid_values}.")
        
    @staticmethod
    def validate_email(email):
        """
        验证电子邮件格式
        """
        import re
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValidationError(f"'{email}' is not a valid email address.")

        