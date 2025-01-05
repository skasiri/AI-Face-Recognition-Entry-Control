import sqlite3
from jdatetime import datetime as jdt


class Subscription:
    def __init__(self):
        conn = sqlite3.connect('db/main.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER,
                start_date TEXT,
                end_date TEXT,
                number_of_sessions INTEGER,
                remaining_sessions INTEGER
            )
        ''')
        conn.close()


    def add_subscription(self, person_id, start_date_jalali, end_date_jalali, number_of_sessions, remaining_sessions):

        start_date_parts = start_date_jalali.split('-')
        start_date_gregorian = jdt(
            int(start_date_parts[0]), int(start_date_parts[1]), int(start_date_parts[2])
        ).togregorian().strftime("%Y-%m-%d")

        end_date_parts = end_date_jalali.split('-')
        end_date_gregorian = jdt(
            int(end_date_parts[0]), int(end_date_parts[1]), int(end_date_parts[2])
        ).togregorian().strftime("%Y-%m-%d")
    
        conn = sqlite3.connect('db/main.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO subscriptions (person_id, start_date, end_date, number_of_sessions, remaining_sessions)
            VALUES (?, ?, ?, ?, ?)
        ''', (person_id, start_date_gregorian, end_date_gregorian, number_of_sessions, remaining_sessions))
        conn.commit()
        conn.close()


    def get_active_subscription(self, person_id):
        conn = sqlite3.connect('db/main.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM subscriptions WHERE person_id = ? AND start_date <= date('now') AND end_date >= date('now')
        ''', (person_id,))
        subscription = cursor.fetchone()
        conn.close()
        return subscription
    
    def update_remaining_sessions(self, subscription_id, remaining_sessions):
        conn = sqlite3.connect('db/main.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE subscriptions SET remaining_sessions = ? WHERE id = ?
        ''', (remaining_sessions, subscription_id))
        conn.commit()
        conn.close()

    def update_subscription(self, subscription_id, start_date_jalali, end_date_jalali, number_of_sessions, remaining_sessions):
        start_date_parts = start_date_jalali.split('-')
        start_date_gregorian = jdt(
            int(start_date_parts[0]), int(start_date_parts[1]), int(start_date_parts[2])
        ).togregorian().strftime("%Y-%m-%d")

        end_date_parts = end_date_jalali.split('-')
        end_date_gregorian = jdt(
            int(end_date_parts[0]), int(end_date_parts[1]), int(end_date_parts[2])
        ).togregorian().strftime("%Y-%m-%d")

        conn = sqlite3.connect('db/main.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE subscriptions SET start_date = ?, end_date = ?, number_of_sessions = ?, remaining_sessions = ? WHERE id = ?
        ''', (start_date_gregorian, end_date_gregorian, number_of_sessions, remaining_sessions, subscription_id))
        conn.commit()
        conn.close()

    def delete_subscription(self, subscription_id):
        conn = sqlite3.connect('db/main.db')
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM subscriptions WHERE id = ?
        ''', (subscription_id,))
        conn.commit()
        conn.close()

