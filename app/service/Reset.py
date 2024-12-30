from datetime import datetime
from app.repo.ResetTokenRepo import ResetTokenRepo
from app.repo.UserRepo import UserRepo
from app.exceptions import AuthenticationError, TokenError
from app.utils.token_utils import generate_reset_token
from werkzeug.security import generate_password_hash

class ResetService:
    """
    Handles core business logic for password reset.
    """
    def __init__(self):
        self.user_repo = UserRepo()
        self.verify_token_repo = ResetTokenRepo()

    def create_reset_token_for_user(self, email: str, expire_minutes=30) -> str:
        """
        1. Find the user by email.
        2. Generate a token and expiration time.
        3. Save the token record in the DB.
        4. Return the token.
        """
        user = self.user_repo.get_user_by_email(email)
        if not user:
            # You might raise an error or just return None
            raise AuthenticationError("Invalid email.")

        token, expires_at = generate_reset_token(expire_minutes)
        self.verify_token_repo.save_reset_token(user.user_id, token, expires_at)
        return token

    def reset_password(self, token: str, new_password: str) -> bool:
        """
        1. Retrieve the token record.
        2. Check if the token exists and is not expired.
        3. Update the user's password hash.
        4. Invalidate the token.
        5. Return True if successful.
        """
        token_record = self.verify_token_repo.find_reset_token(token)
        if not token_record:
            # Token not found
            raise TokenError("Invalid token.")

        if token_record.expires_at < datetime.utcnow():
            # Token expired
            raise TokenError("Token expired.")

        user = self.user_repo.get_user_by_id(token_record.user_id)
        if not user:
            raise AuthenticationError("Invalid user.")

        hashed_password = generate_password_hash(new_password)
        self.user_repo.update_user_password(user.user_id, hashed_password)

        # Invalidate the token to prevent reuse
        self.verify_token_repo.invalidate_reset_token(token)

        return True