#!/bin/bash
DB_ADMIN="zephyr" # Database admin username
DB_ADMIN_PASSWORD="password"        # Database admin password
DB_NAME="e2m_db"                    # Database name
DB_USER="e2m"                       # Database user
DB_HOST="localhost"                 # PostgreSQL container hostname

# Check if the database exists, if not, create the database
if PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
  echo "Database '$DB_NAME' already exists."
else
  echo "Database '$DB_NAME' does not exist. Creating database..."
  PGPASSWORD=$DB_ADMIN_PASSWORD createdb -h $DB_HOST -U $DB_ADMIN $DB_NAME
  echo "Database '$DB_NAME' created."
fi

# Enter superuser mode and grant all privileges to user 'e2m'
echo "Granting all privileges to user '$DB_USER' on database '$DB_NAME'..."
PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -d $DB_NAME -c "GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_USER;" 1>/dev/null 2>&1
PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -d $DB_NAME -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 1>/dev/null 2>&1
PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -d $DB_NAME -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;" 1>/dev/null 2>&1
PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -d $DB_NAME -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $DB_USER;" 1>/dev/null 2>&1
PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -d $DB_NAME -c "GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO $DB_USER;" 1>/dev/null 2>&1
echo "All privileges granted to user '$DB_USER' on database '$DB_NAME'."
echo "Database setup complete."

# Define a function to check if an initial migration file exists in the migrations directory
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

# Check the migrations directory and initial migration file
if check_initial_migration; then
  echo "Initial migration exists. Applying migrations..."
  flask db upgrade
else
  echo "Initial migration does not exist or migrations directory not found. Initializing database..."
  rm -rf migrations # Remove existing migrations directory (if any)
  flask db init
  flask db migrate -m "Initial migration."
  flask db upgrade
fi

# try connecting to the database
if PGPASSWORD=$DB_ADMIN_PASSWORD psql -h $DB_HOST -U $DB_ADMIN -d $DB_NAME -c "SELECT 1" 1>/dev/null 2>&1; then
  echo "🚀 Database connection successful."
else
  echo "❌ Database connection failed."
fi
