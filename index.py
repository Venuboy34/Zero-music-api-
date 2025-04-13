import os
import subprocess
import json
from urllib.parse import parse_qs

def handler(request):
    # Get the 'name' from the query params
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

    # Use yt-dlp to search and get music details
    search_command = f'yt-dlp --default-search ytsearch1:"{name}" --get-title --get-id --get-thumbnail'
    process = subprocess.Popen(search_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

    # Get the music data from stdout
    output = stdout.decode().strip().split("\n")
    if len(output) < 3:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "status": "error",
                "message": "Could not find any result"
            }, indent=2)
        }

    title, video_id, thumbnail = output

    mp3_url = f'https://api.vevioz.com/@api/button/mp3/{video_id}'

    # Return only the details and download link
    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "success",
            "result": {
                "title": title,
                "thumbnail": thumbnail,
                "mp3": f'https://dl.musiczero.vercel.app/mp3/{video_id}.mp3'
            }
        }, indent=2)
    }
