# video-loop-player

Plays an mp4 forward, then backward, forever, with no pause at either turnaround.

```
./pingpong.py clip.mp4              # builds clip_pingpong.mp4, then loops it (mpv or ffplay)
./pingpong.py clip.mp4 -o out.mp4   # build only; loop out.mp4 in any player
```

The output is the clip followed by its reverse without the duplicated turnaround
frames, so looping it is seamless. Audio is dropped. Needs `ffmpeg` (and `mpv` or
`ffplay` to play). Reversal buffers the whole clip in memory, so use short clips.

## On iPhone (web app)

`index.html` is a self-contained page that does the same thing in the browser
(ffmpeg.wasm, vendored under `lib/`, no CDN or server-side processing). Host the
repo as static files over HTTPS (e.g. GitHub Pages: Settings → Pages → deploy from
branch), open the URL in Safari, tap **Choose video**, pick a clip from Photos/Files.
Share → **Add to Home Screen** to keep it as an app. Conversion happens on the phone
(first load downloads ~30 MB), so use short clips.
