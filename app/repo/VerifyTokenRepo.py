from typing import Optional
from datetime import datetime
from app.utils.database import get_db_connection
from app.dtos.TokenRecordDto import VerifyTokenRecordDto

class VerifyTokenRepo:
    @staticmethod
    def save_verify_token(email: str, token: str, expires_at: datetime) -> None:
        """
        Insert a verify token record into the database.
        """
        conn = get_db_connection()
        with conn.cursor() as cursor:
            query = """
                INSERT INTO VerifyToken (email, token, expires_at)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (email, token, expires_at))
        conn.commit()

    @staticmethod
    def find_verify_token(token: str) -> Optional[VerifyTokenRecordDto]:
        """
        Retrieve the token record from the database by token string.
        Returns None if not found.
        """
        conn = get_db_connection()
        with conn.cursor() as cursor:
            query = """
                SELECT email, token, expires_at
                FROM VerifyToken
                WHERE token = %s
            """
            cursor.execute(query, (token,))
            row = cursor.fetchone()
            if row is None:
                return None

            # row -> (user_id, token, expires_at)
            return VerifyTokenRecordDto(*row)

    @staticmethod
    def invalidate_verify_token(token: str) -> None:
        """
        Delete the token record from the database (one-time use).
        """
        conn = get_db_connection()
        with conn.cursor() as cursor:
            query = """
                DELETE FROM VerifyToken
                WHERE token = %s
            """
            cursor.execute(query, (token,))
        conn.commit()