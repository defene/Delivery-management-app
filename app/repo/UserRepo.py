from typing import Optional
from app.models.UserModel import UserDto
from app.utils.database import get_db_connection
from app.exceptions import DatabaseError
from werkzeug.security import check_password_hash

class UserRepo:
    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[UserDto]:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT
                        user_id,
                        username,
                        password_hash,
                        email,
                        enabled
                    FROM `User` 
                    WHERE user_id = %s
                """
                cursor.execute(query, (user_id,))
                row = cursor.fetchone()
                if row is None:
                    return None
                
                # row -> (user_id, username, password_hash, email, enabled)
                return UserDto(*row)
        except Exception as e:
            raise DatabaseError(f"Error fetching user by ID {user_id}: {e}")
        

    @staticmethod
    def get_user_by_id(conn, user_id):
        with conn.cursor() as cursor:
            query = """
                SELECT  *
                FROM    User 
                WHERE   user_id = %s
            """
            cursor.execute(query, user_id)
            return cursor.fetchone()


    @staticmethod
    def check_user_exists(user_id: int) -> bool:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT EXISTS (
                        SELECT 1 
                        FROM `User` 
                        WHERE user_id = %s
                    )
                """
                cursor.execute(query, (user_id))
                count = cursor.fetchone()[0]
                return count > 0
        except Exception as e:
            raise DatabaseError(f"Error checking user {user_id}: {e}")

    @staticmethod
    def update_user_by_id_no_password(user_dto: UserDto) -> int:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    UPDATE `User`
                    SET
                        email = %s,
                        username = %s
                    WHERE user_id = %s
                """
                cursor.execute(query, (user_dto.email, user_dto.username, user_dto.user_id))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Error updating user {user_dto.user_id}: {e}")

    @staticmethod
    def get_user_by_email(email: str) -> Optional[UserDto]:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT
                        user_id,
                        username,
                        password_hash,
                        email,
                        enabled
                    FROM `User`
                    WHERE email = %s
                """
                cursor.execute(query, (email,))
                row = cursor.fetchone()
                if row is None:
                    return None
                
                # row -> (user_id, username, password_hash, email, enabled)
                return UserDto(*row)
        except Exception as e:
            raise DatabaseError(f"Error fetching user by email {email}: {e}")

    @staticmethod
    def create_user(email: str, username: str, password_hash: str, first_name: str, last_name: str, role_name: str) -> Optional[int]:
        """
        Create a new user in the database.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO `User` (email, username, password_hash, first_name, last_name)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (email, username, password_hash, first_name, last_name))
                user_id = cursor.lastrowid
                if not user_id:
                    raise DatabaseError("Failed to retrieve the inserted user_id.")
                
                query = """
                    INSERT INTO `Act` (user_id, role_name)
                    VALUES (%s, %s)
                """
                cursor.execute(query, (user_id, role_name))
                
            conn.commit()
            return user_id
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Unexpected error creating user {username}: {e}")

    @staticmethod
    def add_user_role(role_name: str, user_id: int) -> None:
        """
        Add a role to the user in the database.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO `Act` (user_id, role_name)
                    VALUES (%s, %s)
                """
                cursor.execute(query, (user_id, role_name))
        except Exception as e:
            raise DatabaseError(f"Error adding role '{role_name}' to user {user_id}: {e}")

    @staticmethod
    def check_user_role(user_id: int, role_name: str) -> bool:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT EXISTS (
                        SELECT 1 
                        FROM `Act` 
                        WHERE user_id = %s AND role_name = %s
                    )
                """
                cursor.execute(query, (user_id, role_name))
                count = cursor.fetchone()[0]
                return count > 0
        except Exception as e:
            raise DatabaseError(f"Error checking role '{role_name}' for user {user_id}: {e}")

    @staticmethod
    def update_user_password(user_id: int, new_password_hash: str) -> None:
        """
        Update the user's password in the database with the given password_hash.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = """
                    UPDATE `User`
                    SET password_hash = %s
                    WHERE user_id = %s
                """
                cursor.execute(query, (new_password_hash, user_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Error updating password for user {user_id}: {e}")

    def check_user_password(conn, user_id, old_password):
        with conn.cursor() as cursor:
            # 注意：使用 %s 作为参数占位符，并传递一个包含 user_id 的元组
            query = """
                SELECT  password_hash
                FROM    User
                WHERE   user_id = %s
            """
            cursor.execute(query, (user_id,))  # 注意这里的逗号，表示这是一个元组
            result = cursor.fetchone()  # 获取查询结果

            stored_password = result[0]  # 假设密码是查询结果的第一列
            print(stored_password)
            print(old_password)
            # 这里进行密码比较
            if check_password_hash(stored_password, old_password):
                return True
            else:
                return False

    @staticmethod
    def update_user_password(conn, user_id, new_password):
        with conn.cursor() as cursor:
            query = """
                UPDATE  User
                SET     password_hash = %s
                WHERE   user_id = %s
            """
            cursor.execute(query, (new_password, user_id,))
            conn.commit()
            return cursor.rowcount
