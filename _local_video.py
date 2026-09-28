# -*- coding: utf-8 -*-
"""串行调用本地 AnimateDiff 服务生成 6 段画面并下载"""
import json, time, urllib.request, os, sys

BASE = 'http://127.0.0.1:7865'
OUT = r'C:\Users\Administrator\DoubaoWork\chats\2026-09-28\new-chat\gaicai-game\assets\_test'

STYLE = 'Chinese ink painting anime illustration, guochao style, warm golden and teal color palette, dreamy soft light, detailed, stable composition, gentle camera motion'
SHOTS = [
    STYLE + ', dawn city market street, young office worker holding a bunch of green scallions, skyscrapers shaped like rising stock chart lines, warm golden glow',
    STYLE + ', ancient balance scale, one pan holding glowing gold ingot, other pan holding dark stormy waves, sparks of light, slow rotation',
    STYLE + ', several wicker baskets of different colors on a wooden desk, eggs being placed into each basket, soft morning light',
    STYLE + ', excited crowd reaching up in a festive market, colorful tulips and soap bubbles floating, dizzying upward spiral, joyful chaos',
    STYLE + ', black swan gliding on a calm lake, storm clouds gathering in the distance, a red umbrella standing open on the shore, wind blowing',
    STYLE + ', young office worker standing on a rooftop at sunset overlooking the city, holding a ledger book, river of golden coins flowing below, hopeful sky'
]

def post(path, payload):
    req = urllib.request.Request(BASE + path, data=json.dumps(payload).encode('utf-8'),
                                 headers={'Content-Type': 'application/json; charset=utf-8',
                                          'Origin': 'http://127.0.0.1:7865',
                                          'Referer': 'http://127.0.0.1:7865/',
                                          'User-Agent': 'Mozilla/5.0'})
    return json.loads(urllib.request.urlopen(req, timeout=60).read().decode('utf-8'))

def get(path):
    return json.loads(urllib.request.urlopen(BASE + path, timeout=30).read().decode('utf-8'))

def generate_one(idx, prompt, seed):
    r = post('/generate', {'prompt': prompt, 'size': 256, 'frames': 16, 'seed': seed})
    if 'error' in r:
        return None, r['error']
    while True:
        time.sleep(12)
        s = get('/status')
        if s['status'] == 'done':
            return s.get('video'), None
        if s['status'] == 'error':
            return None, s.get('log', 'error')
        sys.stdout.write(f'  shot{idx} ... {s.get("status")}\n'); sys.stdout.flush()

seeds = [42, 2026, 7, 88, 1314, 520]
results = {}
for i, p in enumerate(SHOTS, start=1):
    sys.stdout.write(f'[{i}/6] generating\n'); sys.stdout.flush()
    video, err = generate_one(i, p, seeds[i-1])
    if err:
        print(f'shot{i} FAILED: {err[:200]}')
        results[i] = None
        continue
    fn = os.path.join(OUT, f'shot{i}.mp4')
    urllib.request.urlretrieve(BASE + video, fn)
    print(f'shot{i} OK -> {fn} ({os.path.getsize(fn)} bytes)')
    results[i] = fn
print('ALL_DONE', json.dumps({str(k): (v or 'FAIL') for k, v in results.items()}))
