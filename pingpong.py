#!/usr/bin/env python3
"""Turn an mp4 into a seamless forward-then-backward ("ping-pong") loop.

  pingpong.py in.mp4                 build in_pingpong.mp4 and play it forever
  pingpong.py in.mp4 -o out.mp4      build only (loop it in any player / embed)
  pingpong.py in.mp4 --no-play

The reversed half omits the duplicated turn-around frames (first and last),
so no frame is ever shown twice in a row and the file's end flows straight
back into its start: loop it and there is no pause anywhere. Audio is dropped
(reversed audio is rarely wanted and can't stay seamless with video).
Requires ffmpeg/ffprobe; playback uses mpv or ffplay if installed.
"""
import argparse, json, shutil, subprocess, sys
from pathlib import Path


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def frame_count(path):
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
               "-show_entries", "stream=nb_read_frames", "-of", "json", str(path)])
    return int(json.loads(out)["streams"][0]["nb_read_frames"])


def build(src, dst, crf):
    n = frame_count(src)
    if n < 3:
        sys.exit("Video needs at least 3 frames.")
    # forward: 0..n-1 ; backward: n-2..1 ; then the loop wraps to frame 0.
    fc = (f"[0:v]split[f][b];"
          f"[b]reverse,trim=start_frame=1:end_frame={n - 1},setpts=PTS-STARTPTS[r];"
          f"[f]setpts=PTS-STARTPTS[f2];[f2][r]concat=n=2:v=1:a=0[v]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-filter_complex", fc,
                    "-map", "[v]", "-an", "-c:v", "libx264", "-crf", str(crf),
                    "-pix_fmt", "yuv420p", "-g", "30", "-movflags", "+faststart", str(dst)],
                   check=True)
    print(f"wrote {dst} ({n} frames forward + {n - 2} backward)")


def play(path):
    if shutil.which("mpv"):
        cmd = ["mpv", "--loop-file=inf", "--no-audio", "--fs", str(path)]
    elif shutil.which("ffplay"):
        cmd = ["ffplay", "-loop", "0", "-an", "-fs", str(path)]
    else:
        sys.exit(f"No mpv/ffplay found; loop {path} in any player.")
    subprocess.run(cmd)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", type=Path)
    p.add_argument("-o", "--output", type=Path)
    p.add_argument("--crf", type=int, default=18, help="x264 quality (lower=better, default 18)")
    p.add_argument("--no-play", action="store_true", help="only build the file")
    a = p.parse_args()
    if not a.input.is_file():
        sys.exit(f"No such file: {a.input}")
    for t in ("ffmpeg", "ffprobe"):
        if not shutil.which(t):
            sys.exit(f"{t} not found on PATH")
    out = a.output or a.input.with_name(a.input.stem + "_pingpong.mp4")
    build(a.input, out, a.crf)
    if not a.no_play and a.output is None:
        play(out)


if __name__ == "__main__":
    main()
