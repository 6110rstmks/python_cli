## prerequisite :
## go over orderdict vs dict in python keep.
import sys
import csv
from collections import OrderedDict

output_file = open('output.txt', 'w')


def read_csv(txt) -> dict[str, dict[int, int]]:

    """
    CSVから一行取得して
    サーバ内で1万件程度のメモリが使える前提でdictで保持する
    """

    # A dictionary where the player is the key and the total score is the value
    player_to_ttlscore = {}

    # 入力のヘッダ行が変更される場合を考慮して定数とする。
    PLAYER_ID_COLUMN = 'player_id'
    SCORE_COLUMN = 'score'

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

                # 辞書の中にプレイヤーidがキーとして存在しなければ作成する
                if player_id not in player_to_ttlscore.keys():
                    player_to_ttlscore[player_id] = {}
                    player_to_ttlscore[player_id]['cnt'] = 1
                    player_to_ttlscore[player_id]['total'] = score

                else:
                    player_to_ttlscore[player_id]['cnt'] += 1
                    player_to_ttlscore[player_id]['total'] += score

    except FileNotFoundError:
        sys.exit(1)
        
    return player_to_ttlscore

        

def main():
    
    try:
        player_to_ttlscore = read_csv('dummy1.txt')
    except FileNotFoundError:
        print("ファイルが見つかりませんでした。",file=output_file)
        sys.exit(1)
