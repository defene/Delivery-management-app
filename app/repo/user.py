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