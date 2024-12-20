class BaseService:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "_initialized"):
            self._initialized = True  # 设置初始化标志
            # 放置初始化代码，仅在首次实例化时执行
            print(f"Initializing {self.__class__.__name__}")

