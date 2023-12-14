from datetime import datetime
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build

youtube_api_key = 'AIzaSyAtdHniUqWc5Cg8Ql5jNiYGxgcdxWSsae8'
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

def buscar_videos(query, maxResults):
    # Realiza la búsqueda de videos en YouTube
    request = youtube.search().list(
        q=query,
        type='video',
        part='id',
        maxResults=maxResults
    )
    response = request.execute()
    # Extrae solo los IDs de los resultados de búsqueda
    video_ids = [item['id']['videoId'] for item in response['items']]
    return video_ids

def buscar_videos_simple(query, maxResults):
    # Realiza la búsqueda de videos en YouTube
    request = youtube.search().list(
        q=query,
        type='video',
        part='snippet',
        maxResults=maxResults
    )
    response = request.execute()

    # Extrae títulos y miniaturas de los resultados de búsqueda
    videos = [{'id': item['id']['videoId'], 'title': item['snippet']['title'], 'thumbnail': item['snippet']['thumbnails']['default']['url']} for item in response['items']]

    return videos

def obtener_informacion_videos(video_ids):
    videos_info = []

    for video_id in video_ids:
        # Obtiene información detallada sobre el video
        video_request = youtube.videos().list(
            part='snippet',
            id=video_id
        )
        video_response = video_request.execute()

        if 'items' in video_response and video_response['items']:
            video_snippet = video_response['items'][0]['snippet']
            video_title = video_snippet['title']
            channel_title = video_snippet['channelTitle']
            published_at = video_snippet['publishedAt']
            description = video_snippet.get('description', '')

            # Obtén las etiquetas (tags) del video
            tags = video_snippet.get('tags', [])

            # Obtén la URL del video
            video_url = f'https://www.youtube.com/watch?v={video_id}'

            # Formatea la fecha en el nuevo formato
            formatted_date = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ').strftime('%d-%m-%y')

            videos_info.append({
                'video_id': video_id,
                'video_title': video_title,
                'channel_title': channel_title,
                'published_at': formatted_date,
                'description': description,
                'tags': tags,
                'video_url': video_url
            })

    return videos_info

def obtener_comentarios(video_id, max_results):
    # Verifica si los comentarios están habilitados para el video
    video_request = youtube.videos().list(
        part='snippet',
        id=video_id
    )
    video_response = video_request.execute()

    if 'items' in video_response and video_response['items']:
        if 'commentingEnabled' in video_response['items'][0]['snippet'] and not video_response['items'][0]['snippet']['commentingEnabled']:
            print(f'Comentarios deshabilitados para el video con ID: {video_id}')
            return []

    # Obtiene comentarios de un video utilizando la API de comentarios de YouTube
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=max_results
    )

    try:
        response = request.execute()
    except Exception as e:
        print(f'Error al obtener comentarios para el video con ID {video_id}: {e}')
        return []

    # Extrae información de los comentarios
    comentarios = [item['snippet']['topLevelComment']['snippet']['textDisplay'] for item in response.get('items', [])]

    return comentarios

def transcribir_audio(video_id):
    try:
        # Intenta obtener la transcripción en español
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["es"])
        text = ' '.join([entry['text'] for entry in transcript])
        return text
    except Exception as e:
        print(f'Error al obtener transcripción en español para el video con ID {video_id}: {e}')

        try:
            # Si no se pudo obtener la transcripción en español, intenta obtenerla en inglés
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
            text = ' '.join([entry['text'] for entry in transcript])
            return text
        except Exception as e:
            print(f'Error al obtener transcripción en inglés para el video con ID {video_id}: {e}')
            return None

"""def obtener_transcripcion_youtube(video_id):
    request = youtube.captions().list(
        part='snippet',
        videoId=video_id
    )

    try:
        response = request.execute()
    except Exception as e:
        print(f'Error al obtener transcripción para el video con ID {video_id}: {e}')
        return None

    if 'items' in response and response['items']:
        caption_id = response['items'][0]['id']
        caption_request = youtube.captions().download(
            id=caption_id,
            tfmt='srt'
        )

        try:
            caption_response = caption_request.execute()
        except Exception as e:
            print(f'Error al descargar la transcripción para el video con ID {video_id}: {e}')
            return None

        return caption_response

    return None"""

def main():
    # Realiza una búsqueda de videos en YouTube
    query = input('Ingresa tu búsqueda: ')
    max_results = int(input('Ingresa la cantidad máxima de resultados: '))

    video_ids = buscar_videos(query, max_results)

    if not video_ids:
        print("No se encontraron videos.")
        return

    # Obtiene información detallada para los videos encontrados
    videos_info = obtener_informacion_videos(video_ids)

    # Obtiene comentarios para los videos encontrados
    comentarios_por_video = obtener_comentarios(video_ids, maxResults=5)

    # Muestra la información detallada y los comentarios de los videos
    for info, comentarios_info in zip(videos_info, comentarios_por_video):
        print(f'Video: "{info["video_title"]}"')
        print(f'Canal: {info["channel_title"]}')
        print(f'Fecha de publicación: {info["published_at"]}')
        print(f'Descripción: {info["description"]}')
        print(f'Etiquetas: {info["tags"]}')
        print(f'URL del video: {info["video_url"]}')

        # Muestra los comentarios para el video actual
        print('Comentarios:')
        for comentario in comentarios_info.get('comentarios', []):
            print(f'- {comentario}')

        print()  # Salto de línea entre videos


if __name__ == '__main__':
    main()
