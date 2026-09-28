# -*- coding: utf-8 -*-
"""组装《金融智慧》无配乐版初版短片：6 镜 = 2s 动画(模糊铺底) + 静态画面 + 旁白 + 中文字幕"""
import os, subprocess, json, sys

BASE = r'C:\Users\Administrator\DoubaoWork\chats\2026-09-28\new-chat\gaicai-game'
FF = r'C:\Users\Administrator\DoubaoWork\tools\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe'
FP = r'C:\Users\Administrator\DoubaoWork\tools\ffmpeg-9.0.2-full_build\bin\ffprobe.exe'
WORK = os.path.join(BASE, 'assets', '_build')
os.makedirs(WORK, exist_ok=True)
FONTQ = r"'C\:/Windows/Fonts/msyh.ttc'"

SUBS = [
    '金融，其实从菜市场就开始了。耶鲁《金融市场》，希勒教授说：市场里每一个价格，背后都是人。',
    '高收益从不免费。期望收益等于无风险利率，加上风险补偿——你多赚的每一分，都是风险付你的报酬。',
    '别把鸡蛋放在一个篮子里。资产相关性越低，组合波动越小。这是数学，也是睡好觉的秘诀。',
    '情绪会自我放大：涨，更多人买，更涨。泡沫的尽头，总有人说：这次不一样。',
    '黑天鹅无法预测，只能应对。留足应急金，不上杠杆，市场怎么跌，都伤不到你的根。',
    '真正的智慧，是把生冷的公式，过成温热的日子。理财的终点不是数字，是你的人生。'
]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode != 0:
        print('FAIL:', ' '.join(cmd)[:200])
        print(r.stderr[-1200:])
        sys.exit(1)
    return r

def dur(path):
    r = subprocess.run([FP, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', path], capture_output=True, text=True)
    return float(r.stdout.strip())

parts = []
for i in range(1, 7):
    anim = os.path.join(BASE, 'assets', '_test', f'shot{i}.mp4')
    img = os.path.join(BASE, 'assets', '_img', f'img{i}.jpg')
    voice = os.path.join(BASE, 'assets', '_audio', f'voice{i}.wav')
    vd = dur(voice)
    TOT = round(vd + 1.0, 2)          # 0.5s 前导 + 旁白 + 0.5s 尾留白
    TSTILL = round(TOT - 2.0, 2)      # 静态段时长
    SUBFILE = os.path.join(WORK, f'sub{i}.txt')
    with open(SUBFILE, 'w', encoding='utf-8') as f:
        f.write(SUBS[i-1])
    out = os.path.join(WORK, f'seg{i}.mp4')
    fc = (
        f"[0:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,"
        f"boxblur=luma_radius=25:luma_power=2[bg];"
        f"[0:v]scale=-1:720,pad=1280:720:(ow-iw)/2:(oh-ih)/2[fg];"
        f"[bg][fg]overlay=(W-w)/2:(H-h)/2,trim=duration=2,setpts=PTS-STARTPTS[v1];"
        f"[1:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,"
        f"format=yuv420p,fps=25,trim=duration={TSTILL},setpts=PTS-STARTPTS[v2];"
        f"[v1][v2]concat=n=2:v=1:a=0,"
        f"drawtext=fontfile={FONTQ}:textfile='{SUBFILE.replace(os.sep,'/').replace(':','\\:')}':"
        f"x=(w-text_w)/2:y=h-170:fontsize=42:fontcolor=white:borderw=3:bordercolor=black@0.6:"
        f"shadowx=2:shadowy=2:shadowcolor=black@0.5:line_spacing=8:"
        f"enable='between(t,0.5,{round(TOT-0.2,2)})'[vout];"
        f"[2:a]aresample=48000,adelay=500|500,apad[aout]"
    )
    cmd = [FF, '-y', '-i', anim, '-loop', '1', '-i', img, '-i', voice,
           '-filter_complex', fc, '-map', '[vout]', '-map', '[aout]',
           '-t', str(TOT), '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
           '-pix_fmt', 'yuv420p', '-r', '25', '-c:a', 'aac', '-b:a', '128k', out]
    run(cmd)
    parts.append(out)
    print(f'seg{i} ok tot={TOT} still={TSTILL} voice={vd}')

# 拼接
lst = os.path.join(WORK, 'list.txt')
with open(lst, 'w', encoding='utf-8') as f:
    for p in parts:
        f.write(f"file '{p}'\n")
final = os.path.join(BASE, 'assets', 'wisdom_nomusic.mp4')
run([FF, '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', final])
print('FINAL', final, os.path.getsize(final), 'total_s', round(dur(final), 1))
