#!/bin/bash
DB_ADMIN="e2m"               # Database admin username
DB_ADMIN_PASSWORD="password" # Database admin password
DB_NAME="e2m_db"             # Database name
DB_USER="e2m"                # Database user
DB_HOST="postgres"           # PostgreSQL container hostname

echo "Checking if database '$DB_NAME' exists..."
if PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
  echo "Database '$DB_NAME' already exists."
  # drop db when it exists
  echo "Dropping database '$DB_NAME'..."
  PGPASSWORD=$DB_ADMIN_PASSWORD dropdb -h $DB_HOST -U $DB_ADMIN $DB_NAME
  echo "Database '$DB_NAME' dropped."
  PGPASSWORD=$DB_ADMIN_PASSWORD createdb -h $DB_HOST -U $DB_ADMIN $DB_NAME
  echo "Database '$DB_NAME' created."
else
  echo "Database '$DB_NAME' does not exist. Creating database..."
  PGPASSWORD=$DB_ADMIN_PASSWORD createdb -h $DB_HOST -U $DB_ADMIN $DB_NAME
  echo "Database '$DB_NAME' created."
fi

# echo "Granting all privileges to user '$DB_USER' on database '$DB_NAME'..."
# PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -d $DB_NAME -c "GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_USER;"
# PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -d $DB_NAME -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
# PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -d $DB_NAME -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;"
# PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -d $DB_NAME -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $DB_USER;"
# PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -d $DB_NAME -c "GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO $DB_USER;"
# echo "All privileges granted to user '$DB_USER' on database '$DB_NAME'."
# echo "Database setup complete."

function check_initial_migration {
  if [ -d "migrations" ]; then
    if ls migrations/versions/*initial*.py 1>/dev/null 2>&1; then
      return 0 # Initial migration exists
    else
      return 1 # Initial migration does not exist
    fi
  else
    return 1 # Migrations directory does not exist
  fi
}

if check_initial_migration; then
  echo "Initial migration exists. Applying migrations..."
  flask db upgrade
else
  echo "Initial migration does not exist or migrations directory not found. Initializing database..."
  rm -rf migrations
  flask db init
  flask db migrate -m "Initial migration."
  flask db upgrade
fi

echo "🎉 Database migrations applied."
