#!/bin/bash

DB_ADMIN="e2m" # 数据库管理员用户名
DB_ADMIN_PASSWORD="password" # 数据库管理员密码
DB_NAME="e2m_db" # 数据库名称
DB_USER="e2m" # 数据库用户名
DB_HOST="postgres" # PostgreSQL 容器主机名

# 检查数据库是否已经存在，如果不存在则创建数据库
if PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo "Database '$DB_NAME' already exists."
else
    echo "Database '$DB_NAME' does not exist. Creating database..."
    PGPASSWORD=$DB_ADMIN_PASSWORD createdb -h $DB_HOST -U $DB_ADMIN $DB_NAME
    echo "Database '$DB_NAME' created."
fi

# 进入最高管理员并赋予 e2m 用户所有权限
echo "Granting all privileges to user '$DB_USER' on database '$DB_NAME'..."


PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -d $DB_NAME -c "GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_USER;"
PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -d $DB_NAME -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -d $DB_NAME -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;"
PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -d $DB_NAME -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $DB_USER;"
PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -d $DB_NAME -c "GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO $DB_USER;"

echo "All privileges granted to user '$DB_USER' on database '$DB_NAME'."
echo "Database setup complete."

# 定义一个函数来检查迁移目录中是否存在初始迁移文件
function check_initial_migration {
    if [ -d "migrations" ]; then
        if ls migrations/versions/*initial*.py 1> /dev/null 2>&1; then
            return 0 # 初始迁移文件存在
        else
            return 1 # 初始迁移文件不存在
        fi
    else
        return 1 # 迁移目录不存在
    fi
}

# 检查迁移目录和初始迁移文件
if check_initial_migration; then
    echo "Initial migration exists. Applying migrations..."
    flask db upgrade
else
    echo "Initial migration does not exist or migrations directory not found. Initializing database..."
    rm -rf migrations # 删除现有的迁移目录（如果存在）
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
fi

echo "Database migrations applied."

