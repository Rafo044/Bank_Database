
mysql -p

passvord .....

ALTER USER 'mysql'@'%' IDENTIFIED WITH mysql_native_password BY 'mysql123';
FLUSH PRIVILEGES;


airflow versiyalar eyni olmalıdı 

image airflov 3.0.4
pip install apache-airflow==3.0.4
