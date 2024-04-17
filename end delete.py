import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def authenticate():
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", scopes
    )
    credentials = flow.run_console()
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def upload_video(youtube, file_path, title, description):
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
        },
        "status": {
            "privacyStatus": "private"  # Cambia a "public" para hacerlo público
        }
    }
    media_file = googleapiclient.http.MediaFileUpload(file_path)

    try:
        response = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media_file
        ).execute()
        video_id = response["id"]
        print("Video subido con éxito. ID:", video_id)
        return video_id
    except googleapiclient.errors.HttpError as e:
        print("Error al subir el video:", e)
        return None

if __name__ == "__main__":
    # Autenticación
    youtube = authenticate()

    # Ruta del archivo de video
    video_file_path = "ruta/al/archivo/video.mp4"

    # Título y descripción del video
    video_title = "Mi Juego No Político"
    video_description = "¡Bienvenidos a mi Juego No Político! Un divertido juego para disfrutar con amigos y familiares."

    # Subir video
    video_id = upload_video(youtube, video_file_path, video_title, video_description)
