from pymysql import connect, Error
from pymysql.cursors import DictCursor


class DataBase:
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = int(port)

    def execute(self, query: str, *parameters):
        return self.__execute(query, *parameters).rowcount

    def select_all(self, query: str, *parameters):
        cursor = self.__execute(query, *parameters)
        return cursor.fetchall()

    def select_one(self, query: str, *parameters):
        cursor = self.__execute(query, *parameters)
        return cursor.fetchone()

    def __execute(self, query: str, *parameters):
        try:
            with self.__open_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, parameters)
                    connection.commit()
                    return cursor
        except Error as e:
            print(f"Error while executing query [{query}]: {str(e)}")

    def __open_connection(self):
        try:
            return connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                cursorclass=DictCursor
            )
        except Error as e:
            print(f"Error while opening sql connection: {str(e)}")

    # Organizer management

    def new_organizer(self, user_id, name):
        self.execute('INSERT INTO `organizers` (`user_id`, `name`) VALUES(%s, %s)', user_id, name)

    def get_list_of_organizers(self):
        return self.select_all('SELECT * FROM `organizers`')

    def del_organizer(self, org_id):
        self.execute('DELETE FROM `organizers` WHERE `id` = %s',org_id)

    def get_organizer_data(self, org_id):
        return self.select_one('SELECT `is_user` FROM `organizers` WHERE `user_id` = %s',org_id)

    def switch_user_mode(self, user_id, mode):
        self.execute('UPDATE `organizers` SET `is_user` = %s WHERE `user_id` = %s',mode, user_id)

    # Events management

    def add_event(self, org_id, title, descr, datetime, address, members_number, pay_type, ticket_price, requisites=None):
        self.execute(
            '''INSERT INTO `events`
(`title`, `descr`, `datetime`, `address`, `members_number`, `pay_type`, `requisites`, `ticket_price`, `org_id`)
VALUES(%s, %s, %s, %s, %s, %s, %s, %s,
(SELECT `id` FROM `organizers` WHERE `user_id` = %s))''',
            title, descr, datetime, address, members_number, pay_type, requisites, ticket_price, org_id
        )

    def get_events_by_organizer(self, org_user_id):
        return self.select_all(
            '''SELECT `events`.`id`, `title`, DATE_FORMAT(`events`.`datetime`, "%%d.%%m.%%Y %%H:%%i") as datetime
FROM `events` LEFT JOIN `organizers` ON `events`.`org_id` = `organizers`.`id`
WHERE `organizers`.`user_id` = %s''',
            org_user_id
        )

    def get_all_events(self):
        return self.select_all(
            'SELECT `id`, `title`, DATE_FORMAT(`datetime`, %s) as datetime FROM `events`',
            "%d.%m.%Y %H:%i"
        )

    def get_event_info(self, event_id):
        return self.select_one(
            '''SELECT `events`.`id` AS id, `descr`, `title`, 
            DATE_FORMAT(`datetime`, %s) as datetime, `address`, `members_number`,
            `pay_type`, `requisites`, `ticket_price`, `org_id`, `organizers`.`user_id` AS org_user_id,
            `organizers`.`name` as org_name, `status`, COUNT(`tickets`.`id`) as members 
            FROM `events` JOIN `organizers` ON `events`.`org_id` = `organizers`.`id`
            LEFT JOIN `tickets` ON `tickets`.`event_id` = `events`.`id`
            WHERE `events`.`id` = %s GROUP BY `events`.`id`''',
            "%d.%m.%Y %H:%i", event_id
        )

    def delete_event(self, event_id):
        self.execute('DELETE FROM `events` WHERE `id` = %s',event_id)
        self.execute('DELETE FROM `tickets` WHERE `event_id` = %s',event_id)

    # User management

    def get_user_info(self, user_id):
        return self.select_one(
            '''SELECT `id`, `name`, `username`, `phone`, `user_id`, `referal_to`
FROM `users` WHERE `user_id` = %s''',
            user_id
        )

    def register_user(self, user_id, name, username, referal_to=None):
        self.execute(
            'INSERT INTO `users` (`user_id`, `name`, `username`, `referal_to`) VALUES(%s, %s, %s, %s)',
            user_id, name, username, referal_to
        )

    def edit_user_data(self, user_id, key, value):
        self.execute(f'UPDATE `users` SET {key} = %s WHERE `user_id` = %s',value, user_id)

    def get_referal_data(self, user_id):
        res = {}
        res = res | self.select_one('SELECT `id`, `bonus`, `referal_to` FROM `users` WHERE `user_id` = %s',user_id)
        res = res | {
            'referals': self.select_all(
            'SELECT `name`, `username` FROM `users` WHERE `referal_to` = %s',
            user_id
            )
        }
        return res

    def plus_bonus(self, user_id, bonus):
        self.execute('UPDATE `users` SET `bonus` = `bonus` + %s WHERE `user_id` = %s',bonus, user_id)

    # ticket management

    def new_ticket(self, user_id, event_id, verify=0) -> int:
        self.execute(
            'INSERT INTO `tickets` (`user_id`, `event_id`, `verify`) VALUES (%s, %s, %s)',
            user_id, event_id, verify
        )
        return self.select_one(
            'SELECT `id` FROM `tickets` WHERE `user_id` = %s AND `event_id` = %s ORDER BY `id` DESC',
            user_id, event_id
            )['id']

    def verify_ticket(self, ticket_id):
        self.execute('UPDATE `tickets` SET `verify` = 1 WHERE `id` = %s',ticket_id)

    def get_ticket_info(self, ticket_id):
        return self.select_one(
            '''SELECT `tickets`.`id` AS id, `users`.`user_id` AS user_id, `users`.`name` AS name, `events`.`title`
            AS title, DATE_FORMAT(`events`.`datetime`, "%%d.%%m.%%Y %%H:%%i") AS datetime, `events`.`status` AS status,
            `events`.`ticket_price` AS price FROM `tickets` JOIN `users` ON `users`.`id` = `tickets`.`user_id`
            JOIN `events` ON `events`.`id` = `tickets`.`event_id` WHERE `tickets`.`id` = %s''',
            ticket_id
        )

    def delete_ticket(self, ticket_id):
        self.execute('DELETE FROM `tickets` WHERE `id` = %s', ticket_id)

    def get_tickets_by_user(self, user_id):
        return self.select_all(
            '''SELECT `tickets`.`id` as id, `events`.`title` as title,
            DATE_FORMAT(`events`.`datetime`, "%%d.%%m.%%Y %%H:%%i") as datetime
            FROM `tickets` JOIN `events` ON `events`.`id` = `tickets`.`event_id`
            WHERE `user_id` = (SELECT `id` FROM `users` WHERE `user_id` = %s)''',
            user_id
        )
