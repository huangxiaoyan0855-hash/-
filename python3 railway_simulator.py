
import heapq
import math

# =====================================
# 北摂電気軌道シミュレーター Ver. 1.0
# =====================================

# 駅間のデータ
# (駅A, 駅B, 所要時間[分], 距離[km], 路線名)
TRACKS = [
    ("東泉丘", "社長の家", 3, 1.2, "千里線"),
    ("社長の家", "豊中", 5, 2.5, "千里線"),
    ("豊中", "大阪空港", 6, 3.0, "空港線"),
    ("豊中", "蛍池", 4, 1.8, "宝塚線"),
    ("蛍池", "東淀川中央", 7, 4.0, "東淀川線"),
    ("東泉丘", "千里中央", 5, 2.4, "千里線"),
    ("千里中央", "蛍池", 8, 4.2, "連絡線"),
]

# 駅の接続情報を自動生成
railway = {}

def add_station(station):
    if station not in railway:
        railway[station] = []

def add_track(a, b, minutes, km, line):
    add_station(a)
    add_station(b)

    railway[a].append((b, minutes, km, line))
    railway[b].append((a, minutes, km, line))

for a, b, minutes, km, line in TRACKS:
    add_track(a, b, minutes, km, line)


# 最短所要時間の経路を探す
def find_route(start, goal):
    queue = [(0, start)]
    costs = {start: 0}
    previous = {}

    while queue:
        cost, current = heapq.heappop(queue)

        if cost != costs[current]:
            continue

        if current == goal:
            break

        for neighbor, minutes, km, line in railway[current]:
            new_cost = cost + minutes

            if new_cost < costs.get(neighbor, float("inf")):
                costs[neighbor] = new_cost
                previous[neighbor] = (
                    current, minutes, km, line
                )
                heapq.heappush(
                    queue, (new_cost, neighbor)
                )

    if goal not in costs:
        return None

    # 到着駅から逆向きにたどって経路を復元
    path = []
    current = goal
    total_km = 0

    while current != start:
        prev, minutes, km, line = previous[current]
        path.append((prev, current, minutes, km, line))
        total_km += km
        current = prev

    path.reverse()
    return path, costs[goal], total_km


# 運賃を計算（このシミュレーター独自の仮ルール）
def calculate_fare(km):
    return 150 + math.ceil(km / 2) * 30


def show_stations():
    print("\n=== 駅一覧 ===")
    for station in sorted(railway):
        print("・" + station)


def search_route():
    show_stations()

    start = input("\n出発駅：").strip()
    goal = input("到着駅：").strip()

    if start not in railway or goal not in railway:
        print("駅名が見つかりません！")
        return

    if start == goal:
        print("出発駅と到着駅が同じです。")
        return

    result = find_route(start, goal)

    if result is None:
        print("この2駅を結ぶ経路はありません。")
        return

    path, minutes, km = result

    print("\n========== 経路検索結果 ==========")
    print(f"出発駅：{start}")
    print(f"到着駅：{goal}")
    print(f"所要時間：{minutes}分")
    print(f"営業キロ：約{km:.1f} km")
    print(f"運賃：{calculate_fare(km)}円")
    print("\n経路：")

    print(start, end="")

    for a, b, time, distance, line in path:
        print(f" --[{line}・{time}分]--> {b}")

    print("==================================")


def main():
    while True:
        print("\n===== 北摂電気軌道 =====")
        print("1. 経路検索")
        print("2. 駅一覧")
        print("3. 終了")

        choice = input("番号を選択：").strip()

        if choice == "1":
            search_route()
        elif choice == "2":
            show_stations()
        elif choice == "3":
            print("ご利用ありがとうございました！")
            break
        else:
            print("1〜3を入力してください。")


if __name__ == "__main__":
    main()
