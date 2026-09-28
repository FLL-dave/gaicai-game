# -*- coding: utf-8 -*-
"""组装《金融智慧》短片 v2（全静态 Ken Burns 运镜 + 片头片尾 + 字幕 + 旁白，约90s）"""
import os, subprocess, sys

BASE = r'C:\Users\Administrator\DoubaoWork\chats\2026-09-28\new-chat\gaicai-game'
FF = r'C:\Users\Administrator\DoubaoWork\tools\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe'
FP = r'C:\Users\Administrator\DoubaoWork\tools\ffmpeg-9.0.2-full_build\bin\ffprobe.exe'
WORK = os.path.join(BASE, 'assets', '_build')
os.makedirs(WORK, exist_ok=True)
FONT = r"'C\:/Windows/Fonts/msyh.ttc'"

# 每镜字幕（手动分行，每行<=28字，两行）
SUBS = [
    '金融，其实从菜市场就开始了。\n耶鲁《金融市场》，希勒教授说：市场里每一个价格，背后都是人。',
    '高收益从不免费。期望收益等于无风险利率，\n加上风险补偿——你多赚的每一分，都是风险付你的报酬。',
    '别把鸡蛋放在一个篮子里。\n资产相关性越低，组合波动越小。这是数学，也是睡好觉的秘诀。',
    '情绪会自我放大：涨，更多人买，更涨。\n泡沫的尽头，总有人说：这次不一样。',
    '黑天鹅无法预测，只能应对。留足应急金，不上杠杆，\n市场怎么跌，都伤不到你的根。',
    '真正的智慧，是把生冷的公式，过成温热的日子。\n理财的终点不是数字，是你的人生。'
]
# 每镜运镜：in=推近, pan_l=右->左平移(zoom1.08), pan_r=左->右平移
MOTION = ['in', 'pan_r', 'in', 'pan_l', 'in', 'in']

def run(cmd, tag):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode != 0:
        err = ' || '.join(l for l in r.stderr.splitlines() if 'rror' in l)[:800]
        print(f'FAIL[{tag}]:', err)
        sys.exit(1)

def dur(path):
    r = subprocess.run([FP, '-v', 'error', '-show_entries', 'format=duration', '-of',
                        'default=noprint_wrappers=1:nokey=1', path], capture_output=True, text=True)
    return float(r.stdout.strip())

parts = []

# ---------- 片头 3s ----------
head = os.path.join(WORK, 'head.mp4')
vf_head = (
    f"drawtext=fontfile={FONT}:text='金融智慧 · 90 秒':x=(w-text_w)/2:y=h/2-110:"
    f"fontsize=66:fontcolor=white:shadowx=3:shadowy=3:shadowcolor=black@0.6:alpha='min(t/1.2,1)',"
    f"drawtext=fontfile={FONT}:text='—— 从菜市场到人生的投资课 ——':x=(w-text_w)/2:y=h/2+20:"
    f"fontsize=34:fontcolor=0xE8C96A:shadowx=2:shadowy=2:shadowcolor=black@0.5:alpha='min(t/1.6,1)',"
    f"fade=t=in:st=0:d=0.6,fade=t=out:st=2.4:d=0.6"
)
run([FF, '-y', '-f', 'lavfi', '-i', 'color=c=black:s=1280x720:r=25:d=3',
     '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
     '-vf', vf_head, '-t', '3', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
     '-pix_fmt', 'yuv420p', '-r', '25', '-c:a', 'aac', '-b:a', '128k', '-shortest', head], 'head')
parts.append(head)
print('head ok')

# ---------- 6 镜 ----------
for i in range(1, 7):
    img = os.path.join(BASE, 'assets', '_img', f'img{i}.jpg')
    voice = os.path.join(BASE, 'assets', '_audio', f'voice{i}.wav')
    vd = dur(voice)
    TOT = round(vd + 3.0, 2)   # 1s 前导 + 旁白 + 2s 尾留白
    frames = int(TOT * 25)
    SUBFILE = os.path.join(WORK, f'sub{i}.txt')
    with open(SUBFILE, 'w', encoding='utf-8') as f:
        f.write(SUBS[i-1])
    motion = MOTION[i-1]
    if motion == 'in':
        zexpr = "min(zoom+0.0008,1.14)"
        xexpr = "iw/2-(iw/zoom/2)"
        yexpr = "ih/2-(ih/zoom/2)"
    elif motion == 'pan_r':   # 从左向右平移
        zexpr = "1.08"
        xexpr = f"(iw-iw/zoom)*on/{frames-1}"
        yexpr = "ih/2-(ih/zoom/2)"
    else:                      # pan_l 从右向左平移
        zexpr = "1.08"
        xexpr = f"(iw-iw/zoom)*(1-on/{frames-1})"
        yexpr = "ih/2-(ih/zoom/2)"
    out = os.path.join(WORK, f'seg{i}.mp4')
    vf = (
        f"zoompan=z='{zexpr}':x='{xexpr}':y='{yexpr}':d=1:s=1280x720:fps=25,"
        f"format=yuv420p,"
        f"drawtext=fontfile={FONT}:textfile='{SUBFILE.replace(os.sep,'/').replace(':','\\:')}':"
        f"x=(w-text_w)/2:y=h-160:fontsize=40:fontcolor=white:box=1:boxcolor=black@0.38:boxborderw=14:"
        f"line_spacing=10:enable='between(t,0.5,{round(TOT-0.2,2)})',"
        f"fade=t=in:st=0:d=0.5,fade=t=out:st={round(TOT-0.5,2)}:d=0.5"
    )
    run([FF, '-y', '-loop', '1', '-t', str(TOT), '-i', img, '-i', voice,
         '-filter_complex',
         f"[0:v]{vf}[vout];[1:a]aresample=48000,adelay=1000|1000,apad[aout]",
         '-map', '[vout]', '-map', '[aout]', '-t', str(TOT),
         '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
         '-r', '25', '-c:a', 'aac', '-b:a', '128k', out], f'seg{i}')
    parts.append(out)
    print(f'seg{i} ok tot={TOT} voice={vd}')

# ---------- 片尾 4s ----------
tail = os.path.join(WORK, 'tail.mp4')
vf_tail = (
    f"drawtext=fontfile={FONT}:text='理财的终点，不是数字，是你的人生。':x=(w-text_w)/2:y=h/2-80:"
    f"fontsize=48:fontcolor=white:shadowx=3:shadowy=3:shadowcolor=black@0.6:alpha='min(t/1.2,1)',"
    f"drawtext=fontfile={FONT}:text='《韭菜大冒险》· 耶鲁《金融市场》观后':x=(w-text_w)/2:y=h/2+40:"
    f"fontsize=30:fontcolor=0xE8C96A:shadowx=2:shadowy=2:shadowcolor=black@0.5:alpha='min(t/1.8,1)',"
    f"fade=t=in:st=0:d=0.6,fade=t=out:st=3.4:d=0.6"
)
run([FF, '-y', '-f', 'lavfi', '-i', 'color=c=black:s=1280x720:r=25:d=4',
     '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
     '-vf', vf_tail, '-t', '4', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
     '-pix_fmt', 'yuv420p', '-r', '25', '-c:a', 'aac', '-b:a', '128k', '-shortest', tail], 'tail')
parts.append(tail)
print('tail ok')

# ---------- 拼接 ----------
lst = os.path.join(WORK, 'list2.txt')
with open(lst, 'w', encoding='utf-8') as f:
    for p in parts:
        f.write(f"file '{p}'\n")
final = os.path.join(BASE, 'assets', 'wisdom_nomusic.mp4')
run([FF, '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', final], 'concat')
print('FINAL', final, os.path.getsize(final), 'total_s', round(dur(final), 1))
