"""Обёртка над mpv для воспроизведения аудио."""
import subprocess
import os
import shutil

class MpvPlayer:
    def __init__(self):
        self.proc = None
        self.current = None
        self.mpv_bin = shutil.which("mpv") or "mpv"

    def play(self, path):
        self.stop()
        if not os.path.exists(path):
            return False
        try:
            self.proc = subprocess.Popen(
                [self.mpv_bin, "--no-video", "--really-quiet", path],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            self.current = path
            return True
        except Exception as e:
            print("mpv error:", e)
            return False

    def stop(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        self.proc = None

    def pause(self):
        """Отправляет SIGSTOP (пауза) или SIGCONT (продолжить)."""
        if not self.proc or self.proc.poll() is not None:
            return
        import signal
        try:
            if self._paused:
                self.proc.send_signal(signal.SIGCONT)
                self._paused = False
            else:
                self.proc.send_signal(signal.SIGSTOP)
                self._paused = True
        except Exception:
            pass

    _paused = False

    def is_playing(self):
        return self.proc is not None and self.proc.poll() is None
