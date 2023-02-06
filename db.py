import sqlite3


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('service-availability.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS service 
        (service_id INTEGER PRIMARY KEY, service_name VARCHAR(50))
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS status 
        (service_id INTEGER, request_time DATETIME, status_code VARCHAR(5), description VARCHAR(30))
        ''')
        self.conn.commit()

    # Получаем список отслеживаемых сервисов
    def service_list(self):
        self.cursor.execute('''
        SELECT service_name FROM service
        ''')
        return [i[0] for i in self.cursor.fetchall()]

    # Добавляем сервис в базу данных
    def add_service(self, service):
        self.cursor.execute('''INSERT INTO service (service_name) VALUES (?)''', (service,))
        self.conn.commit()

    # Удаляем сервис из базы данных
    def delete_service(self, service):
        self.cursor.execute('''
        DELETE FROM service WHERE service_name = (?)''', (service,))
        self.conn.commit()

    # Добавляем записи о новом состоянии сервисов
    def update_services(self, info):
        for services in info:
            self.cursor.execute('''
            SELECT request_time, status_code FROM status WHERE service_id = 
            (SELECT service_id from service WHERE service_name = ?) 
            ORDER BY request_time DESC LIMIT 1''', (services,))
            status_chek = self.cursor.fetchall()
            if status_chek[0][1] == info[services]["code"]:
                self.cursor.execute('''
                UPDATE status SET request_time = datetime('now') WHERE 
                request_time = ? AND service_id = (SELECT service_id from service WHERE service_name = ?)
                ''', (status_chek[0][0], services))
            else:
                record = (services, info[services]["code"], info[services]["description"])
                self.cursor.execute('''
                INSERT INTO status (service_id, request_time, status_code, description) VALUES 
                ((SELECT service_id from service WHERE service_name = ?), datetime('now'), ?, ?)''', record)
        self.conn.commit()

    # Получаем статус сервиса
    def status_service(self, services):
        self.cursor.execute('''
        SELECT description FROM status WHERE''')

    # Получаем историю об изменении состояния сервиса
    def story_status(self, service):
        self.cursor.execute('''
        SELECT request_time, status_code, description FROM status
        WHERE service_id = (SELECT service_id from service WHERE service_name = ?)
        ORDER BY request_time DESC LIMIT 50''', (service,))
        s = self.cursor.fetchall()
        return {service: {i[0]: {"status_code": i[1], "description": i[2]} for i in s}}
