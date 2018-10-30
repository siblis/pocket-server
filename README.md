# pocket-server
Pocket Messenger Server Part

Серверная часть месенджера для гиков.

Функции сервера

  Работает по протоколу https, основной серверный язык python, СУБД используем postgresql.

Требования:
  postgresql>=9.6
  python 3.6
    tornado
    sqlalchemy

Установка серверной части:
  Подготавливаем сервер баз данных
  
   Можно развернуть в виртаульной машине virtualbox, VMWare Workstation и пр. операционная система Ubuntu/Debian.
    
    Устанавливаем postgresql сервер: 
      sudo apt install postgresql
  
   Создадим пользователя для базы данных и чистую базу:
   
    sudo su -u postgres
    psql
    select * from pg_user;    #посмотреть список пользователей
    CREATE ROLE washuser WITH PASSWORD 'myPassword';      #создаем пользователя и придумываем ему пароль
    CREATE DATABASE dbname OWNER washuser;                #создаем новую БД
    GRANT CONNECT ON DATABASE dbname TO washuser;         #даем права новому пользователю на БД
   
   Если разработку ведете не на том же сервер, что и сервер баз данных, то настраиваем конфиги postgresql сервера. 
   Редактируем файл /etc/postgresql/9.6/main/postgresql.conf
    
    ищем строчку #listen_addresses = 'localhost'
    убираем коментарий и указываем IP адресс вашего postgresql сервера, должно получиться что-то в роде
    listen_addresses = '192.168.0.22, localhost'	
    коментим все строчки с ssl_ (если конечно, не планируете шифрование организовывать до своего сервера 
    СУБД, для разработки это как приавило не нужно)
   
   Дальше редактируем файл /etc/postgresql/9.6/main/pg_hba.conf:
   
    добавляем в конце файла указав ip машины с которой конектитесь к серверу
    host	 all		 all		 192.168.Х.Х/32	password
    
   На всякий пожарный проверяем запущен ли сервер postgresql:
    
    sudo systemctl enable postgresql
    sudo systemctl restart postgresql
   
   Теперь переходим к файлам нашего проекта, клонируем файлы проекта:
   
    git clone https://github.com/siblis/pocket-server.git
   
   Заходим в корневую папку проекта pocket-server ищем дублируем файл salt.py.template в salt.py
   Меняем в файле salt.py строку с salt = "nachtohotite"
   Дальше нужно создать модели/структуры в БД, для этого копируем файл database_tools/db_config.py.template в 
   database_tools/db_config.py
   Редактируем файл - указываем параметры подключения к вашему серверу баз данных.
   Если HTTPS не используете, то необходимо в файле server.py, его то же отключить, строчка http_server должна
   выглядить так:
   
        http_server = tornado.httpserver.HTTPServer(Application())
    
   Да, не забудьте установить необходимые библиотеки:
    
    sudo pip3 install tornado, sqlalchemy
    если pip3 не установлен его можено утановит так:
    sudo apt update
    sudo apt install python3-pip
    
   Дальше можно запустить файл init.py из папки database_tools. Он создаст в базе данных нужные таблицы.
   
   После чего можено запустить основной файл сервера - server.py
    
    Start server
   
   Сервер запущен. Доступен по адресу 127.0.0.1:8888

  
