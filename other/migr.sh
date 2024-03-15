rm -rf migrations toolmux.db
flask db init
flask db migrate -m "Models"
flask db upgrade
