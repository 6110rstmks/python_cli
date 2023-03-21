from collections import OrderedDict
import csv
import sys

def csv_read(txt) -> dict[str, dict[int, int]]:

    """
    CSVから一行取得して
    サーバ内で1万件程度のメモリが使える前提でdictで保持する
    """

    # 入力のヘッダ行が変更される場合を考慮して定数とする。
    PLAYER_ID_COLUMN = 'player_id'
    SCORE_COLUMN = 'score'

    # A dictionary where the player is the key and the total score is the value
    player_to_ttlscore = {}

    try:
        with open(txt) as csv_file:
            # 一行目を捨てる
            csv.DictReader(csv_file)

            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:


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

                get_player_ttlscore(player_id, score, player_to_ttlscore)

    except FileNotFoundError:
        sys.exit(1)

    return player_to_ttlscore

def get_player_ttlscore(player_id: str, score: int, player_to_ttlscore):

    # 辞書の中にプレイヤーidがキーとして存在しなければ作成する
    if player_id not in player_to_ttlscore.keys():
        player_to_ttlscore[player_id] = {}
        player_to_ttlscore[player_id]['cnt'] = 1
        player_to_ttlscore[player_id]['total'] = score

    else:
        player_to_ttlscore[player_id]['cnt'] += 1
        player_to_ttlscore[player_id]['total'] += score


def get_avgscore(player_to_ttlscore: dict[str, dict[int, int]]) -> OrderedDict[int, list[str]]:

    """
    プレイヤーをキー、値をトータルスコアとする辞書を入力値として
    平均値をキー、プレイヤーを値とする辞書を返す
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
            avgscore_to_player[avg_score] = [player]

        else:
            avgscore_to_player[avg_score].append(player)

    return OrderedDict(sorted(avgscore_to_player.items(), reverse=True))


def output_ranking(avgscore_to_player: dict[int, list[str]]) -> list[str]:

    output_data = []

    REPORT_RANKINGS = 10

    rank: int = 1

    for avg_score, player_with_samescore in avgscore_to_player.items():

        if rank > REPORT_RANKINGS:
            break

        for player_id in player_with_samescore:

            output_data.append("{} {} {}".format(rank, player_id, avg_score))

        rank += len(player_with_samescore)

    return output_data
