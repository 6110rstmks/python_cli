## prerequisite :
## go over orderdict vs dict in python keep.

import csv
from collections import OrderedDict

output_file = open('src/output.txt', 'w')

def get_total_score(csv_reader) -> dict[str, dict[int, int]]:

    """
    CSVから一行取得して
    サーバ内で1万件程度のメモリが使える前提でdictで保持する
    """

    # 入力のヘッダ行が変更される場合を考慮して定数とする。
    PLAYER_ID_COLUMN = 'player_id'
    SCORE_COLUMN = 'score'

    # A dictionary where the player is the key and the total score is the value
    player_to_ttlscore = {}
    for row in csv_reader:


        print(len(row))


        try:
            player_id: str = row[PLAYER_ID_COLUMN]
            score: int = int(row[SCORE_COLUMN])
        except:
            # 三項目のscoreが数値でない場合処理が止まってしまうため次の行へ
            # エラー出力は仕様に記載されていないので省略する

            continue

        """
        テンポラリデータベースが使えるか記載されていないので、
        メモリに辞書として保持する。
        """

        # 辞書の中にプレイヤーidがキーとして存在しなければ作成する
        if player_id not in player_to_ttlscore.keys():
            player_to_ttlscore[player_id] = {}
            player_to_ttlscore[player_id]['cnt'] = 1
            player_to_ttlscore[player_id]['total'] = score

        else:
            player_to_ttlscore[player_id]['cnt'] += 1
            player_to_ttlscore[player_id]['total'] += score

        
    print(player_to_ttlscore)
    return player_to_ttlscore

def get_avgscore(player_to_ttlscore: dict[str, dict[int, int]]) -> OrderedDict[int, list[str]]:


    """
    プレイヤーをキー、値をトータルスコアとする辞書を入力値として
    平均値をキー、プレイヤーを値とする辞書（orderDict）を返す
    """

    avgscore_to_player: dict[int, str] = {}

    # for player in player_to_ttlscore:
    # こっちのほうがキーか値かどちらをループするのかわかりやすい
    for player in player_to_ttlscore.keys():

        if player_to_ttlscore[player]['cnt'] == 0:
            # 0除算対策
            continue

        avg_score: int = int(player_to_ttlscore[player]['total'] / player_to_ttlscore[player]['cnt'])

        if avg_score not in avgscore_to_player.keys():

            # 同じ平均スコアをもつプレイヤーが他に存在する場合 

            avgscore_to_player[avg_score] = [player]

        else:
            avgscore_to_player[avg_score].append(player)

    print(OrderedDict(sorted(avgscore_to_player.items(), reverse=True)))

    ## 平均値の降順にする
    ## https://stackoverflow.com/questions/9001509/how-do-i-sort-a-dictionary-by-key
    return OrderedDict(sorted(avgscore_to_player.items(), reverse=True))

def output_ranking(avgscore_to_player: OrderedDict[int, list[str]]):

    print(avgscore_to_player)

    """
    平均点によるランキングを作成
    同一スコアの場合、同一ランキングとする。
    同点の平均スコアのプレイヤーが居た場合において、10名以上のランキングが作られる事がある
    """

    # capital letters represent a constant
    # 仕様変更を見越した定数

    REPORT_RANKINGS = 10

    rank: int = 1

    for avg_score, player_with_samescore in avgscore_to_player.items():

        # ランキング10で終了
        if rank > REPORT_RANKINGS:
            break

        for player_id in player_with_samescore:
            print("{},{},{}".format(rank, player_id, avg_score), file=output_file)

        # 同じスコアの数だけ、プレイヤー分、ランクの数を増やす
        rank += len(player_with_samescore)

try:
    with open('src/dummy1.txt') as csv_file:

        # 一行目を捨てる
        csv.DictReader(csv_file)

        csv_reader = csv.DictReader(csv_file, delimiter=',')

        player_to_ttlscore: dict[str, dict[int, int]] = get_total_score(csv_reader)

        avgscore_to_player: OrderedDict[int, list[str]] = get_avgscore(player_to_ttlscore)

        output_ranking(avgscore_to_player)

        print('finish')

except FileNotFoundError:
    print("file is not found",file=output_file)

# テストコードのかきやすいコードを書くために副作用の少ないコードを書くよう心がけた
# （グローバル変数が関数内にあるということはないはず）

# I keep in mind to write code with less side-effect to make it easy to write tesutable code 




