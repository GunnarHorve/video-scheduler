# :clapper: Video Scheduler -- Make TV Special Again
Binge watching is depressing and not satisfying.  Watch your series one episode at a time, at the same time every day.

# :running: Running the program
```
  pip install -r requirements.txt
  python main.py --cast="Living Room TV"
```

# :memo: Managing the queue
Active video queue is managed through the file [video-queue.txt](https://github.com/GunnarHorve/video-scheduler/blob/master/video-queue.txt).  Whenever your scheduled play time arrives, the top line is removed and your corresponding video played.

videos should be 1 per line, consisting of only the [video id](https://commentpicker.com/youtube-video-id.php#:~:text=A%20Youtube%20Video%20ID%20is,Youtube%20video%20on%20any%20website.).  Ultimately, your `video-queue.txt` file should look something like:
```
dQw4w9WgXcQ
-32NGYLqwAQ
m47x5rG4NyM
fGAl9__U8Uk
1akbNBqsP48
```

If you're looking for some inspiration, some curated playlists can be found in the [playlists](https://github.com/GunnarHorve/video-scheduler/tree/master/playlists) folder of this repository.
