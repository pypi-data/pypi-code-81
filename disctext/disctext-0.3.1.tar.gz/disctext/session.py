import os
import signal
import asyncio
import discord
import argparse

from eventkit import Event
from contextlib import suppress


from .video import *
from .models import *


signal.signal(signal.SIGINT, signal.SIG_DFL)


class Session(discord.Client):

    STARTUP: float = 3.0
    TIMEOUT: float = 7.5

    def __init__(self, settings: Settings, **kwargs):
        self.settings = settings
        self.video = Video(settings)
        super().__init__(**kwargs)
        self.update = Event("update")

    async def monitor(self):
        await self.wait_until_ready()
        print("\n=> Connected")
        task = self.loop.create_task(self.pipeline())
        await asyncio.sleep(Session.STARTUP)
        while task:
            updated = None
            with suppress(asyncio.TimeoutError):
                updated = await asyncio.wait_for(
                    self.update, Session.TIMEOUT)
            if not updated:
                self.update.set_done()
                await asyncio.sleep(1.5)
                task.cancel()
                with suppress(asyncio.CancelledError):
                    await task
                task = None
                break

        print("=> Disconnected")
        await self.close()
        self.loop.stop()

    async def pipeline(self):
        video, settings = self.video, self.settings
        target = self.get_channel(int(settings.channel))
        minutes = int(video.frames * (video.rate.max + video.rate.min)/120)
        print(f'=> Starting "{video.filename}" in #{target}\n'
              f'=> Reading {video.remaining} frames\n'
              f'=> ETA: ~{minutes} minute(s)\n\n'
              f'=> Note: Progress bar excludes invalid (skipped) frames\n')

        capture = Capture(video)
        canvas = Canvas(video)
        pipe = capture.pipe(canvas)

        bar = Progress(video)
        bar.set_source(self.update)

        await target.send(f'NOW PLAYING: "{video.filename}"')

        capture.start()
        async for frame in pipe.aiter():
            await target.send(frame)
            await asyncio.sleep(video.rate.limit())
            self.update.emit(True)

    def run(self):
        self.settings.check()
        self.loop.create_task(self.monitor())
        self.loop.run_until_complete(
            self.start(self.settings.token))


def run(
        media: os.PathLike,
        token: str,
        channel: int,
        highlight: syntax = None,
        inverted: bool = False,
        min_cols: int = 40,
        max_cols: int = 100,
        min_area: int = 1,
        max_area: int = 1950,
        min_rate: float = 0.8,
        max_rate: float = 1.0) -> None:

    settings = Settings(
        media,
        token,
        channel,
        highlight,
        inverted,
        min_cols,
        max_cols,
        min_area,
        max_area,
        min_rate,
        max_rate
    )
    session = Session(settings)
    session.run()


def envars(path: str = ".env") -> Settings:
    """ 
    Make settings from environment variables.
    """

    import dotenv
    dotenv.load_dotenv(dotenv.find_dotenv(path))

    settings = Settings(
        os.getenv("MEDIA"),
        os.getenv("TOKEN"),
        os.getenv("CHANNEL"),
        os.getenv("HIGHLIGHT", ""),
        os.getenv("INVERT", False),
        os.getenv("MIN_COLS", 40),
        os.getenv("MAX_COLS", 100),
        os.getenv("MIN_AREA", 1),
        os.getenv("MAX_AREA", 1950),
        os.getenv("MIN_RATE", 0.8),
        os.getenv("MAX_RATE", 1.0)
    )

    return settings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--media", "-m", type=str, required=True)
    parser.add_argument("--token", "-t", type=str, required=True)
    parser.add_argument("--channel", "-c", type=int, required=True)
    parser.add_argument("--highlight", type=str, default="")
    parser.add_argument("--inverted", type=bool, default=False)
    parser.add_argument("--cols", nargs="+", type=int, default=(40, 100))
    parser.add_argument("--area", nargs="+", type=int, default=(1, 1950))
    parser.add_argument("--rate", nargs="+", type=float, default=(0.8, 1.0))
    args = parser.parse_args()
    settings = Settings(args.media,
                        args.token,
                        args.channel,
                        args.highlight,
                        args.inverted,
                        *tuple(args.cols),
                        *tuple(args.area),
                        *tuple(args.rate))
    session = Session(settings)
    session.run()


if __name__ == "__main__":
    main()
