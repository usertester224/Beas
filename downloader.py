#!/usr/bin/env python3
"""Simple yt-dlp downloader."""
from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path
from typing import Iterable, List

from yt_dlp import YoutubeDL

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download media with yt-dlp.")
    parser.add_argument("url", help="Media URL to download")
    parser.add_argument(
        "-o",
        "--output-dir",
        default="downloads",
        help="Output directory (default: downloads)",
    )
    parser.add_argument(
        "-f",
        "--format",
        default="best",
        help="yt-dlp format selector (default: best)",
    )
    parser.add_argument(
        "--audio",
        action="store_true",
        help="Extract audio only (mp3)",
    )
    parser.add_argument(
        "--no-playlist",
        action="store_true",
        help="Do not download playlists",
    )
    parser.add_argument(
        "--telegram",
        action="store_true",
        help="Send downloaded files to Telegram via MTProto",
    )
    parser.add_argument(
        "--telegram-chat",
        default="me",
        help="Target Telegram chat ID or @username (default: Saved Messages)",
    )
    return parser.parse_args()

def build_options(args: argparse.Namespace, downloaded: List[Path]) -> dict:
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    def progress_hook(status: dict) -> None:
        if status.get("status") == "finished":
            filename = status.get("filename")
            if filename:
                downloaded.append(Path(filename))

    options: dict = {
        "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
        "format": args.format,
        "noplaylist": args.no_playlist,
        "progress_hooks": [progress_hook],
    }

    if args.audio:
        options.update(
            {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
        )

    return options

def download_media(args: argparse.Namespace) -> List[Path]:
    downloaded: List[Path] = []
    options = build_options(args, downloaded)

    with YoutubeDL(options) as ydl:
        ydl.download([args.url])

    return downloaded

def telegram_config(args: argparse.Namespace) -> dict:
    return {
        "api_id": int(os.environ["TG_API_ID"]),
        "api_hash": os.environ["TG_API_HASH"],
        "session": os.environ["TG_SESSION"],
        "chat": args.telegram_chat,
    }

def chunked(iterable: Iterable[Path], size: int = 1) -> Iterable[List[Path]]:
    batch: List[Path] = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch

async def send_to_telegram(files: Iterable[Path], config: dict) -> None:
    from telethon import TelegramClient
    from telethon.sessions import StringSession

    async with TelegramClient(
        StringSession(config["session"]),
        config["api_id"],
        config["api_hash"],
    ) as client:
        target = config["chat"]
        for batch in chunked(files, size=10):
            for path in batch:
                file_handle = await client.upload_file(
                    str(path),
                    part_size_kb=1024,
                )
                await client.send_file(target, file_handle, caption=path.name)

def main() -> None:
    args = parse_args()
    downloaded = download_media(args)

    if args.telegram and downloaded:
        config = telegram_config(args)
        asyncio.run(send_to_telegram(downloaded, config))

if __name__ == "__main__":
    main()