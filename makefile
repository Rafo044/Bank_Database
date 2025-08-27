up:
	docker compose up -d --build

create:
	mkdir -p ./logs  ./airflow-db ./plugins ./postgres_data ./data ./mysql_data
	sudo chown -R 50000:0 ./logs ./dags ./airflow-db ./plugins ./postgres_data ./data
	sudo chmod -R 777 ./logs ./dags ./airflow-db ./plugins ./postgres_data ./data ./mysql_data

clean:
	sudo rm -rf ./logs  ./airflow-db ./plugins ./postgres_data ./data ./mysql_data


down:
	docker compose down --volumes

logs:
	docker compose logs -f


restart: down up
	
