"""環境変数を読み込むためのモジュール
"""

from atlus import setting
import os
import dotenv

# `~/.env` に環境変数ファイルが存在している前提のコード
dotenv.load_dotenv(os.path.join(setting.PROJECT_ROOT, '.env'))

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT', 3306)
MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB_NAME = os.getenv('MYSQL_DB_NAME', 'leanonme')
