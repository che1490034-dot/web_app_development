import os
from dotenv import load_dotenv
from app import create_app
from app.models import db

# 載入環境變數
load_dotenv()

app = create_app()

def init_db():
    with app.app_context():
        db.create_all()
        print("Initialized the database.")

if __name__ == '__main__':
    # 開發模式下啟動，自動初始化 DB
    init_db()
    app.run(debug=True)
