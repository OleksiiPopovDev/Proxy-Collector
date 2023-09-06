docker-compose -f docker-compose.yml up --build -d

# shellcheck disable=SC2046
while ! docker exec -it $(grep CONTAINER_NAME_MYSQL .env | cut -d '=' -f2) sh -c "export MYSQL_PWD=$MYSQL_PASS; mysql -uroot < /var/database/mysql.db" --silent; do
  echo "Waiting 10 seconds for start of MySQL and check again!"
  sleep 10
  attempts=$((attempts + 1))
  if [ $attempts = 5 ]; then
    echo "Can't configure mysql database. Skip configuration database and continue installation? (yes/no)"
    read SKIP_CONFIGURATI

    if [ "$SKIP_CONFIGURATION" = "yes" ]; then
      break
    fi
  fi
done