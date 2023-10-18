from src.channel import Channel


class Video:
    def __init__(self, video_id):
        video_info = Channel.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=video_id
                                                         ).execute()

        self.id = video_id
        self.title = video_info['items'][0]['snippet']['title']
        self.url = "https://youtu.be/" + str(video_id)
        self.view_count = video_info['items'][0]['statistics']['commentCount']
        self.like_count = video_info['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        playlist_videos = Channel.get_service().playlistItems().list(playlistId=playlist_id,
                                                                     part='contentDetails',
                                                                     maxResults=50,
                                                                     ).execute()

        if video_id in [video['contentDetails']['videoId'] for video in playlist_videos['items']]:
            super().__init__(video_id)
            self.playlist_id = playlist_id
        else:
            raise Exception("Video not found")
