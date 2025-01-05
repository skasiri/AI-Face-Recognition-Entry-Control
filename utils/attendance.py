import datetime
import sqlite3
import pandas as pd
from jdatetime import datetime as jdt
from utils.encodings import get_persons
from utils.subscription import Subscription
from entry_list_frame import clear_attendance_rows, add_attendance_row

class AttendanceTracker:
    def __init__(self):
        self.attendance_list = []
        self.current_date = datetime.date.today()

    def add_attendance(self, melli, face_image):
        print('Add attendance for: ', melli)

        # Load today's attendance data from excel
        self.load_todays_attendance()
        print('Todays attendance loaded', len(self.attendance_list))

        # if today's date has changed, reset the attendance list
        if self.current_date != datetime.date.today():
            self.attendance_list = []
            self.current_date = datetime.date.today()

        
        conn = sqlite3.connect('db/main.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM persons WHERE melli = ?', (melli,))
        person = cursor.fetchone()

        if not person:
            return
        
        subscription_text = 'NO SUBSCRIPTION'
        sub = Subscription()
        active_subscription = sub.get_active_subscription(melli)
        print(active_subscription)
        if active_subscription:
            if active_subscription[5] > 0:
                subscription_text = 'SUBSCRIBED'
                new_active_subscription = list(active_subscription)
                new_active_subscription[5] -= 1
                active_subscription = tuple(new_active_subscription)
                sub.update_remaining_sessions(active_subscription[0], active_subscription[5])
        

        name = person[1] + " " + person[2]
        mobile = person[3]
        exist_item = None

        for item in self.attendance_list:
            if int(item['melli']) == int(melli):
                exist_item = item
                break
        if exist_item:
            exist_item['lastSeenAt'] = datetime.datetime.now()
            exist_item['persianDate'] = jdt.now().strftime("%Y-%m-%d")
            exist_item['timeSpent'] = str(exist_item['lastSeenAt'] - exist_item['enterAt']).split('.')[0]
            
            self.save_to_excel()
        else:
            persian_date = jdt.now().strftime("%Y-%m-%d")
            self.attendance_list.append({
                'name': name,
                'melli': int(melli),
                'mobile': mobile,
                'enterAt': datetime.datetime.now(),
                'lastSeenAt': datetime.datetime.now(),
                'persianDate': persian_date,
                'timeSpent': '0 days 00:00:00',
                'subscription': subscription_text,
                'allowedSessions': active_subscription[4],
                'remainingSessions': active_subscription[5]
            })
            self.save_to_excel()
            add_attendance_row(int(melli), name, mobile,datetime.datetime.now(), datetime.datetime.now(), '0 days 00:00:00')

        conn.close()

    def update_attendance(self, melli):
        print('update_attendance for: ', melli)

        # if today's date has changed, reset the attendance list
        if self.current_date != datetime.date.today():
            self.add_attendance(melli)
            return

        self.load_todays_attendance()
        
        for item in self.attendance_list:
            if int(item['melli']) == int(melli):
                item['lastSeenAt'] = datetime.datetime.now()
                item['timeSpent'] = str(item['lastSeenAt'] - item['enterAt']).split('.')[0]
                persian_date = jdt.now().strftime("%Y-%m-%d")
                item['persianDate'] = persian_date

                self.save_to_excel()
                break

    def save_to_excel(self):
        persian_date = jdt.now().strftime("%Y-%m-%d")
        file_path = f"Export/{persian_date}.xlsx"
        df = pd.DataFrame(self.attendance_list)
        df.to_excel(file_path, index=False)

    def load_from_excel(self, file_path):
        try:
            # Load today's attendance data from excel
            df = pd.read_excel(file_path)
            self.attendance_list = df.to_dict('records')

            # Clear the table
            clear_attendance_rows()
            # Add the loaded data to the table
            for item in self.attendance_list:
                add_attendance_row(item['melli'], item['name'], item['mobile'], item['enterAt'], item['lastSeenAt'], item['timeSpent'])

        except FileNotFoundError:
            pass

    def load_todays_attendance(self):
        persian_date = jdt.now().strftime("%Y-%m-%d")
        file_path = f"Export/{persian_date}.xlsx"
        self.load_from_excel(file_path)

