class UserRepo:
    @staticmethod
    def get_user_by_id(conn, user_id):
        with conn.cursor() as cursor:
            query = """
                SELECT
                    *
                FROM User 
                WHERE user_id = %s
            """
            cursor.execute(query, user_id)
            return cursor.fetchone()
        
    @staticmethod
    def update_user_by_id_no_password(conn, user_dto):
        with conn.cursor() as cursor:
            query = """
                UPDATE User
                SET
                    email = %s,
                    username = %s
                WHERE user_id = %s
            """
            cursor.execute(query, (user_dto.email, user_dto.username, user_dto.user_id))
            conn.commit()
            return cursor.rowcount

    