import logging
from flask import Blueprint, jsonify, request
from ..dtos.LoginDto import LoginDto
from ..dtos.RegisterDto import RegisterDTO
from app.service.Login import LoginService
from app.service.Reset import ResetService
from app.service.Register import RegisterService
from app.utils.validation import Validator
from app.utils.ses_email_utils import send_email_ses
from app.decorators import token_required, roles_required
from app.exceptions import handle_exception

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
login_service = LoginService()
reset_service = ResetService()
register_service = RegisterService()


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        required_fields = ["email", "password", "role_name"]
        Validator.validate_required_fields(data, required_fields)
        
        validation_rules = {
            "email": (True, str),
            "password": (True, str),
            "role_name": (True, str)
        }
        Validator.validate_query_params(data, validation_rules)
        Validator.validate_email(data["email"])

        user_dto = LoginDto(
            email=data["email"],
            password=data["password"],
            role_name=data["role_name"]
        )

        response = login_service.authenticate_user(user_dto)

        return jsonify(response), 200
    except Exception as e:
        return handle_exception(e)
    
@auth_bp.route('/register/user', methods=['POST'])
def register_user():
    try:
        data = request.json

        required_fields = ["username", "password", "email", "first_name", "last_name", "verify_token"]
        Validator.validate_required_fields(data, required_fields)
        Validator.validate_email(data["email"])

        register_dto = RegisterDTO(
            username=data["username"],
            password=data["password"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            role_name="user",
            verify_token=data["verify_token"],
        )

        register_service.register_user(register_dto)

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return handle_exception(e)
    
@auth_bp.route("/verify-token", methods=["POST"])
def verify_token():
    """
    1. Get 'email' from request body.
    2. Generate a verify token if user exists.
    3. Send the reset link via AWS SES (or do nothing if user not found).
    4. Return a generic success message (avoid revealing if user exists).
    """
    try:
        data = request.json
        required_fields = ["email"]
        Validator.validate_required_fields(data, required_fields)
        
        validation_rules = {
            "email": (True, str)
        }
        Validator.validate_query_params(data, validation_rules)
        Validator.validate_email(data["email"])
        
        email = data["email"]

        # Generate a verification code for the user
        verification_code = register_service.create_verify_token_for_user(email)
        
        if verification_code:
            # Prepare email details
            sender_email = "cyiheng312@gmail.com"  # Must be verified in SES
            subject = "Verify Your Email Address"
            
            # Plain text email content
            body_text = (
                f"Hello,\n\n"
                f"Thank you for registering. Please use the following verification code to verify your email address:\n\n"
                f"{verification_code}\n\n"
                f"If you did not request this, please ignore this email.\n\n"
                f"Best regards,\n"
                f"Your Company Name"
            )
            
            # HTML email content
            body_html = f"""
            <html>
            <body>
                <p>Hello,</p>
                <p>Thank you for registering. Please use the following verification code to verify your email address:</p>
                <h2>{verification_code}</h2>
                <p>If you did not request this, please ignore this email.</p>
                <p>Best regards,<br>Your Company Name</p>
            </body>
            </html>
            """
            
            # Call AWS SES utility function to send the email
            success = send_email_ses(
                sender=sender_email,
                recipient=email,
                subject=subject,
                body_text=body_text,
                body_html=body_html,
                region_name="us-east-1"  # Replace with your AWS SES region
            )
            
            if not success:
                logger.warning(f"Failed to send verification email to {email}")
        
        # Always return a generic message to avoid revealing whether the email exists
        return jsonify({"message": "If that email is valid, we've sent a verification code."}), 200

    except Exception as e:
        # Handle exceptions gracefully
        return handle_exception(e)

    
@auth_bp.route('/register/staff', methods=['POST'])
@token_required
@roles_required("staff")
def register_staff():
    try:
        data = request.jsonD

        required_fields = ["username", "email", "first_name", "last_name"]
        Validator.validate_required_fields(data, required_fields)
        Validator.validate_email(data["email"])

        register_dto = RegisterDTO(
            username=data["username"],
            password="",
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            role_name="staff",
        )

        register_dto = register_service.register_user(register_dto)            
        
        sender_email = "cyiheng312@gmail.com"
        subject = "Your Account Registration Details"
        body_text = (
            f"Hello {register_dto.first_name},\n\n"
            f"Your account has been created with the following details:\n"
            f"Email: {register_dto.email}\n"
            f"Password: {register_dto.password}\n\n"
            f"Please log in and change your password immediately.\n\n"
            f"Best regards,\n"
            f"Your Company Team"
        )
        body_html = (
            f"<p>Hello {register_dto.first_name},</p>"
            f"<p>Your account has been created with the following details:</p>"
            f"<ul>"
            f"<li><strong>Email:</strong> {register_dto.email}</li>"
            f"<li><strong>Password:</strong> {register_dto.password}</li>"
            f"</ul>"
            f"<p>Please log in and change your password immediately.</p>"
            f"<p>Best regards,<br>Your Company Team</p>"
        )
        
        success = send_email_ses(
            sender=sender_email,
            recipient=register_dto.email,
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            region_name="us-east-1"  # Replace with your region
        )
        if not success:
            # Optionally, handle the failure (e.g., rollback user creation, retry, log, etc.)
            print(f"Failed to send registration email to {register_dto.email}")

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return handle_exception(e)
    
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    """
    1. Get 'email' from request body.
    2. Generate a reset token if user exists.
    3. Send the reset link via AWS SES (or do nothing if user not found).
    4. Return a generic success message (avoid revealing if user exists).
    """
    try:
        data = request.json
        required_fields = ["email"]
        Validator.validate_required_fields(data, required_fields)
        
        validation_rules = {
            "email": (True, str)
        }
        Validator.validate_query_params(data, validation_rules)
        Validator.validate_email(data["email"])
        
        email = data["email"]

        token = reset_service.create_reset_token_for_user(email)
        if token:
            # Build reset link
            reset_link = f"http://localhost:5000/static/reset-password.html?token={token}"

            # Prepare email details
            sender_email = "cyiheng312@gmail.com"  # Must be verified in SES
            subject = "Reset Your Password"
            body_text = f"Click here to reset your password:\n{reset_link}"
            body_html = f"""
            <html>
            <body>
                <p>Click the following link to reset your password:</p>
                <a href="{reset_link}">{reset_link}</a>
            </body>
            </html>
            """

            # Call AWS SES utility function
            success = send_email_ses(
                sender=sender_email,
                recipient=email,
                subject=subject,
                body_text=body_text,
                body_html=body_html,
                region_name="us-east-1"  # Replace with your region
            )
            if not success:
                logger.warning(f"Failed to send reset email to {email}")

        # Always return a generic message
        return jsonify({"message": "If that email is valid, we've sent a link."}), 200
    except Exception as e:
        return handle_exception(e)

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    """
    1. Get 'token' and 'new_password' from request body.
    2. Pass to ResetService to handle logic.
    3. Return success or error response accordingly.
    """
    try:
        print("reset password")
        
        data = request.json
        required_fields = ["token", "new_password"]
        Validator.validate_required_fields(data, required_fields)
        
        validation_rules = {
            "token": (True, str),
            "new_password": (True, str)
        }
        Validator.validate_query_params(data, validation_rules)
        
        token = data["token"]
        new_password = data["new_password"]

        print(token)
        print(new_password)
        success = reset_service.reset_password(token, new_password)
        print(success)
        
        if success:
            return jsonify({"message": "Password reset successful"}), 200
        else:
            return jsonify({"message": "Invalid or expired token"}), 400
    except Exception as e:
        return handle_exception(e)