import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

        response = self.get_info()

        self.title = response['items'][0]['snippet']['title']
        self.description =response['items'][0]['snippet']['description']
        self.url = response['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscriber_count = response['items'][0]['statistics']['subscriberCount']
        self.video_count = response['items'][0]['statistics']['videoCount']
        self.view_count = response['items'][0]['statistics']['viewCount']

    @classmethod
    def get_service(cls):
        service = build('youtube', 'v3', developerKey=cls.api_key)
        return service

    def get_info(self):
        youtube = self.get_service()
        response = youtube.channels().list(
            id=self.channel_id,
            part='snippet,statistics'
        ).execute()
        return response

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        response = self.get_info()
        print(json.dumps(response, indent=2, ensure_ascii=False))

    def to_json(self, file_name):
        channel_dict = {'channel_id': self.channel_id, 'title': self.title, 'description': self.description,
                        'url': self.url, 'subscriber_count': self.subscriber_count, 'video_count': self.video_count,
                        'view_count': self.view_count}
        with open(file_name, "w", encoding='utf8') as f:
            json.dump(channel_dict, f, ensure_ascii=False)

