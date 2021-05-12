import vk_api
import time
import pandas as pd
import datetime
import os.path


class VkUser:
    def __init__(self, u_id):
        self.u_id = u_id
        self.last_online = -1
        self.online = False

    def get_id(self):
        return self.u_id


def create_users():
    import config
    global user_list
    for c_id in config.Ids:
        user_list.append(VkUser(c_id))
        print('[NEW USER] %s' % str(c_id))


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


def create_config():
    if not os.path.exists('data'):
        os.makedirs('data')
    
    if not os.path.exists('config.py'):
        with open('config.py', 'w') as f:
            f.write("""EPS = 10\nIds = []\nTOKEN = ''""")
        print('Config file created, please insert token and user ids')
        raise SystemExit


def main():
    import config
    global user_list
    time_fix = time.time()
    vk_session = vk_api.VkApi(token=config.TOKEN)

    vk = vk_session.get_api()

    platforms = {1: 'mobile', 2: 'iPhone', 3: 'iPad', 4: 'Android', 5: 'Windows Phone', 6: 'Windows 10', 7: 'website'}

    for current_user in user_list:
        u_id = current_user.get_id()
        if os.path.exists('./data/%s.csv' % (str(u_id))):
            data_table = pd.read_csv('./data/%s.csv' % (str(u_id)), index_col=0)
        else:
            data_table = pd.DataFrame()
        time_now = datetime.datetime.now()
        c_time = datetime.datetime.strftime(time_now, '%H:%M:%S')
        c_date = datetime.datetime.strftime(time_now, '%d/%m/%Y')
        user_object = vk.users.get(user_ids=u_id, fields='last_seen')
        u_time = user_object[0]['last_seen']['time']
        platform_id = user_object[0]['last_seen']['platform']
        u_name = user_object[0]['first_name'] + ' ' + user_object[0]['last_name']
        platform = platforms[platform_id]
        time_object = datetime.datetime.fromtimestamp(u_time)
        is_online = time_now < (time_object + datetime.timedelta(seconds=config.EPS))
        if is_online != current_user.online:
            print('[STATUS] %s is now %s' % (u_name, 'online' if is_online else 'offline'))
            current_user.online = is_online
        new_data_table = pd.DataFrame({'user_id': [u_id, ], 'date': [c_date, ], 'time': [c_time, ],
                                       'online': [is_online, ], 'platform': [platform, ],
                                       'last_seen': [u_time, ], 'timestamp': [datetime.datetime.timestamp(time_now), ]})
        data_table = data_table.append(new_data_table, ignore_index=True)
        data_table.to_csv('./data/%s.csv' % (str(u_id)))
    time_now = datetime.datetime.now()
    print('[DONE] %s' % (datetime.datetime.strftime(time_now, '%H:%M:%S %d/%m/%Y')))
    time_fix -= time.time()
    time.sleep(config.EPS + time_fix if abs(time_fix) < config.EPS else config.EPS)


if __name__ == "__main__":
    user_list = []
    create_config()
    create_users()
    while True:
        try:
            main()
        except Exception as e:
            print('[ERROR] %s' % (e))
            time.sleep(30)
