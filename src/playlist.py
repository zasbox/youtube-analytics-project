import isodate

from src.channel import Channel

from datetime import datetime, timedelta


class PlayList:
    youtube = Channel.get_service()

    def __init__(self, playlist_id):
        self.__playlist_videos = PlayList.youtube.playlistItems().list(playlistId=playlist_id,
                                                                       part='contentDetails, snippet',
                                                                       maxResults=50,
                                                                       ).execute()

        self.playlist_id = playlist_id
        self.title = self.__playlist_videos['items'][0]['snippet']['title'].split('.')[0]
        self.url = "https://www.youtube.com/playlist?list=" + str(playlist_id)

    @property
    def total_duration(self):
        video_list = self.get_video_list()

        total_duration = timedelta()

        for video in video_list['items']:
            iso_8601_duration = video['contentDetails']['duration']
            total_duration += isodate.parse_duration(iso_8601_duration)
        return total_duration

    def show_best_video(self):
        video_list = self.get_video_list()

        id_video_with_max_rate = max([[video['statistics']['likeCount'], video['id']] for video in video_list['items']],
                                     key=lambda v: v[0])[1]
        url = "https://youtu.be/" + id_video_with_max_rate
        return url

    def get_video_list(self):
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.__playlist_videos['items']]
        video_response = PlayList.youtube.videos().list(part='contentDetails,statistics',
                                                        id=','.join(video_ids)
                                                        ).execute()
        return video_response
