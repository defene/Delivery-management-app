class DashBoardService:
    def __init__(self, db):
        self.db = db

    def get_dashboard(self):
        return self.db.get_dashboard()