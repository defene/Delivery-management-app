from flask import Flask
# from .routes import category_routes, item_routes, order_routes, user_routes
from flask_cors import CORS
from .utils.database import init_db, import_sql_file, hash_and_update_passwords, create_database

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

    # 初始化数据库
    config = app.config
    create_database(
        host=config['MYSQL_HOST'],
        port=config['MYSQL_PORT'],
        user=config['MYSQL_USER'],
        password=config['MYSQL_PASSWORD'],
        database_name=config['MYSQL_DB']
    )
    init_db(app)

    # 导入数据库结构
    with app.app_context():
        import_sql_file()
        hash_and_update_passwords()

    # # 注册路由
    # app.register_blueprint(user_routes.user_bp)
    # app.register_blueprint(item_routes.item_bp)
    # app.register_blueprint(category_routes.category_bp)
    # app.register_blueprint(order_routes.order_bp)

    return app