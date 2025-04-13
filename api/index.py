import os
import subprocess
import json
from urllib.parse import parse_qs

def handler(request):
    params = parse_qs(request.query_string.decode())
    name = params.get('name', [None])[0]

    if not name:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "status": "error",
                "message": "Please provide a music name using ?name="
            }, indent=2)
        }

    command = f'yt-dlp --default-search ytsearch1:"{name}" --get-title --get-id --get-thumbnail'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "status": "error",
                "message": "Failed to fetch music",
                "error": stderr.decode()
            }, indent=2)
        }

    output = stdout.decode().strip().split("\n")
    if len(output) < 3:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "status": "error",
                "message": "No valid results"
            }, indent=2)
        }

    title, video_id, thumbnail = output

    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "success",
            "result": {
                "title": title,
                "thumbnail": thumbnail,
                "mp3": f"https://dl.musiczero.vercel.app/mp3/{video_id}.mp3"
            }
        }, indent=2)
    }
