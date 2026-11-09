# video-loop-player

Plays an mp4 forward, then backward, forever, with no pause at either turnaround.

```
./pingpong.py clip.mp4              # builds clip_pingpong.mp4, then loops it (mpv or ffplay)
./pingpong.py clip.mp4 -o out.mp4   # build only; loop out.mp4 in any player
```

The output is the clip followed by its reverse without the duplicated turnaround
frames, so looping it is seamless. Audio is dropped. Needs `ffmpeg` (and `mpv` or
`ffplay` to play). Reversal buffers the whole clip in memory, so use short clips.
