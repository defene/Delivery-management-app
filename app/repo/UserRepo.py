from werkzeug.security import check_password_hash


class UserRepo:
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

    @staticmethod
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
