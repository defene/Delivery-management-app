from typing import Optional
from datetime import datetime
from app.utils.database import get_db_connection
from app.dtos.TokenRecordDto import TokenRecordDto

class ResetTokenRepo:
    @staticmethod
    def save_reset_token(user_id: int, token: str, expires_at: datetime) -> None:
        """
        Insert a reset token record into the database.
        """
        conn = get_db_connection()
        with conn.cursor() as cursor:
            query = """
                INSERT INTO ResetToken (user_id, token, expires_at)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (user_id, token, expires_at))
        conn.commit()

    @staticmethod
    def find_reset_token(token: str) -> Optional[TokenRecordDto]:
        """
        Retrieve the token record from the database by token string.
        Returns None if not found.
        """
        conn = get_db_connection()
        with conn.cursor() as cursor:
            query = """
                SELECT user_id, token, expires_at
                FROM ResetToken
                WHERE token = %s
            """
            cursor.execute(query, (token,))
            row = cursor.fetchone()
            if row is None:
                return None

            # row -> (user_id, token, expires_at)
            return TokenRecordDto(*row)

    @staticmethod
    def invalidate_reset_token(token: str) -> None:
        """
        Delete the token record from the database (one-time use).
        """
        conn = get_db_connection()
        with conn.cursor() as cursor:
            query = """
                DELETE FROM ResetToken
                WHERE token = %s
            """
            cursor.execute(query, (token,))
        conn.commit()