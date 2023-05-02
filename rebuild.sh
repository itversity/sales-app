export SALES_DB_HOST=saleshost
export SALES_DB_PORT=5432
export SALES_DB_NAME=sales_db
export SALES_DB_USER=sales_user
export SALES_DB_PASS=itversity

docker compose down -v --rmi all
docker compose up -d --build