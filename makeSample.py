import datetime

import radar

import random

# source_file = open('dummy1.txt', 'a')
source_file = open('dummy1.txt', 'w')


start_date = datetime.datetime(2021, 1, 1)
stop_date = datetime.datetime(2021, 12, 31)

# print(type(radar.random_datetime(start_date, stop_date)))
date_li = []

date_li.append(str(radar.random_datetime(start_date, stop_date)))
date_li.append(str(radar.random_datetime(start_date, stop_date)))
date_li.append(str(radar.random_datetime(start_date, stop_date)))
date_li.append(str(radar.random_datetime(start_date, stop_date)))

print(date_li)


for i in range(100):

    # 2021/03.09 02;45 のようなフォーマット
    new_date_data = ("/".join(str(radar.random_datetime(start_date, stop_date)).split("-")))[:-3]

    # print(new_date_data)

    score = round(random.randint(1, 20000) / 1000) * 1000

    player_id = ("{:0>4}".format(random.randint(1, 10000)))

    player_id = 'player' + str(player_id)
    print("{},{},{}".format(new_date_data, player_id, score), file=source_file)

source_file.close()


