class Config:
    SECRET_KEY = 'your_secret_key'   # 必须设置，避免 Flask 抛出警告
    DEBUG = True                    # 启用调试模式
    MYSQL_HOST = 'localhost'        # 数据库主机
    MYSQL_PORT = 3306               # 数据库端口
    MYSQL_USER = 'root'        # 数据库用户
    MYSQL_PASSWORD = '123456'
    MYSQL_DB = 'Delivery'