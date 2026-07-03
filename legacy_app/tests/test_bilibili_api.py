"""临时测试脚本：验证 B站 API 连通性和视频信息获取。"""
from curl_cffi.requests import Session

s = Session(impersonate="chrome")
# 获取 buvid
s.get("https://www.bilibili.com/")
r = s.get("https://api.bilibili.com/x/frontend/finger/spi")
data = r.json()["data"]
s.cookies.set("buvid3", data["b_3"], domain=".bilibili.com")
s.cookies.set("buvid4", data["b_4"], domain=".bilibili.com")

# 测试三个目标视频
test_cases = [
    ("BV1zPD6BzEZy", "短视频1 (awesome-design-md)"),
    # 稍后会解析 b23.tv/LmGncCM 和 b23.tv/m1QoLsK
]

for bvid, label in test_cases:
    api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    r = s.get(api_url)
    info = r.json()
    print(f"\n=== {label} ===")
    print(f"Code: {info.get('code')}")
    if info.get("code") == 0:
        d = info["data"]
        print(f"Title: {d.get('title')}")
        print(f"Duration: {d.get('duration')}s")
        print(f"Parts: {d.get('videos')}")
        for p in d.get("pages", [])[:5]:
            print(f"  P{p['page']}: {p['part']} ({p['duration']}s)")

        # 获取弹幕 cid
        cid = d.get("cid")
        print(f"  Main CID: {cid}")

        # 获取评论数
        aid = d.get("aid")
        stat = d.get("stat", {})
        print(f"  AID: {aid}")
        print(f"  Views: {stat.get('view')}, Danmakus: {stat.get('danmaku')}, Replies: {stat.get('reply')}")
    else:
        print(f"Error: {info.get('message')}")

# 测试短链接解析
print("\n=== 短链接解析 ===")
import subprocess
for short_url, label in [
    ("https://b23.tv/LmGncCM", "短视频2"),
    ("https://b23.tv/m1QoLsK", "长视频系列"),
]:
    result = subprocess.run(
        ["curl", "-sIL", "-o", "NUL", "-w", "%{url_effective}", short_url],
        capture_output=True, text=True, timeout=15,
    )
    final_url = result.stdout.strip()
    print(f"{label}: {final_url}")

    # 从 URL 提取 BV 号
    import re
    m = re.search(r"BV(\w+)", final_url)
    if m:
        bvid = "BV" + m.group(1)
        api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
        r = s.get(api_url)
        info = r.json()
        if info.get("code") == 0:
            d = info["data"]
            print(f"  Title: {d.get('title')}")
            print(f"  Duration: {d.get('duration')}s, Parts: {d.get('videos')}")
            for p in d.get("pages", [])[:3]:
                print(f"    P{p['page']}: {p['part']} ({p['duration']}s)")
            stat = d.get("stat", {})
            print(f"  Danmakus: {stat.get('danmaku')}, Replies: {stat.get('reply')}")
