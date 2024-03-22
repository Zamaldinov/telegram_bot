from yandex_music import Client
import os
from typing import List, Dict
from yandex_music.track_short import TrackShort


class Controller:
    def __init__(self):
        token = os.environ.get('TOKEN')
        self.client = Client(token).init()

    @staticmethod
    def track_short_to_string(track_short_list: List[TrackShort], header: str) -> str:
        """Возвращает список треков"""
        result = [header]
        for track_short in track_short_list:
            track, chart = track_short.track, track_short.chart
            artists = ''
            if track.artists:
                artists = ' - ' + ', '.join(artist.name for artist in track.artists)

            track_text = f'{track.title}{artists}'
            track_text = f'{chart.position} {track_text}'
            result.append(track_text)
        return '\n'.join(result)

    def get_last_ten_chart_tracks(self, chart_id: str) -> str:
        """Возвращает последние 10 треков из чарта"""
        chart = self.client.chart(chart_id).chart
        result = chart.tracks[-10:]
        return self.track_short_to_string(result, 'Последние 10 треков чарта:')

    def get_first_ten_chart_tracks(self, chart_id: str) -> str:
        """Возвращает первые 10 треков из чарта"""
        chart = self.client.chart(chart_id).chart
        result = chart.tracks[:11]
        return self.track_short_to_string(result, 'Первые 10 треков чарта:')

    def get_genre_dictionary_from_chart(self, chart_id: str) -> Dict[str, List[TrackShort]]:
        """Возвращает словарь жанров и треков"""
        genre_dict = {}
        chart = self.client.chart(chart_id).chart
        for track_short in chart.tracks:
            genre = track_short.track.albums[0]['genre']
            if genre not in genre_dict:
                genre_dict[genre] = [track_short]
            else:
                genre_dict[genre].append(track_short)
        return genre_dict

    def get_all_chart(self, chart_id: str) -> str:
        """Возвращает чарт треков красивым списком"""
        chart = self.client.chart(chart_id).chart
        text = [f'🏆 {chart.title}', chart.description, '', 'Треки:']
        for track_short in chart.tracks:
            track, chart = track_short.track, track_short.chart
            artists = ''
            if track.artists:
                artists = ' - ' + ', '.join(artist.name for artist in track.artists)

            track_text = f'{track.title}{artists}'

            if chart.progress == 'down':
                track_text = '🔻 ' + track_text
            elif chart.progress == 'up':
                track_text = '🔺 ' + track_text
            elif chart.progress == 'new':
                track_text = '🆕 ' + track_text
            elif chart.position == 1:
                track_text = '👑 ' + track_text

            track_text = f'{chart.position} {track_text}'
            text.append(track_text)

        return '\n'.join(text)

    def commands_list(self):
        """Возвращает список команд для бота"""
        commands = ['/chart - показывает список чарт песен в выбранном регионе.',
                    '/low - показывает последние 10 треков.',
                    '/high - показывает первые 10 треков.',
                    '/custom - показать треки чарта конкретного жанра.',
                    '/change - смена региона.',
                    '/history показывает историю запрошенных команд (10 запросов).']
        result = ''
        for i_list in commands:
            result += i_list + '\n'
        return result


