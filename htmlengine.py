from jinja2 import Template
from views import View


class HtmlEngine:

    ALBUMS = '''
        <div id="albums-container">
                    {% for album in data %}
                    <div class="albums-container-item">
                        <div class="albums-container-item-img-container">
                            {% if album['album_art'] %}
                            <img class="albums-container-item-img" src="{{ album['album_art'] }}">
                            {% else %}
                            <svg xmlns="http://www.w3.org/2000/svg"
                                class="albums-container-item-img albums-container-item-svg" width="24" height="24"
                                viewBox="0 0 24 24" stroke-width="1.5" stroke="#ffffff" fill="none" stroke-linecap="round"
                                stroke-linejoin="round">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                                <circle cx="12" cy="12" r="9" />
                                <circle cx="12" cy="12" r="1" />
                                <path d="M7 12a5 5 0 0 1 5 -5" />
                                <path d="M12 17a5 5 0 0 0 5 -5" />
                            </svg>
                            {% endif %}
                            <svg xmlns="http://www.w3.org/2000/svg" class="albums-container-item-btn-play" height="24px"
                                viewBox="0 0 24 24" width="24px" fill="#000000">
                                <path
                                    d="M8 6.82v10.36c0 .79.87 1.27 1.54.84l8.14-5.18c.62-.39.62-1.29 0-1.69L9.54 5.98C8.87 5.55 8 6.03 8 6.82z" />
                            </svg>

                        </div>
                        <div class="albums-container-item-bottom">
                            <p class="albums-container-item-album">{{ album['album'] }}</p>
                            <p class="albums-container-item-artist">{{ album['album_artist'] }}</p>
                            <svg xmlns="http://www.w3.org/2000/svg" class="albums-container-item-dots" width="24"
                                height="24" viewBox="0 0 24 24" stroke-width="1.5" stroke="#fff" fill="none"
                                stroke-linecap="round" stroke-linejoin="round">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                                <circle cx="5" cy="12" r="1" />
                                <circle cx="12" cy="12" r="1" />
                                <circle cx="19" cy="12" r="1" />
                            </svg>
                        </div>
                    </div>
                    {% endfor %}
                </div>
    '''

    ALBUM_DETAILS = '''
        <div id="album-details-container">
                    <div class="album-details-album-meta">
                        <div class="album-details-albumart-container">
                        {% if data['album_art'] %}
                            <img class="album-details-albumart" src="{{ data['album_art'] }}">
                        {% else %}
                            <svg xmlns="http://www.w3.org/2000/svg"
                                class="album-details-albumart album-details-albumart-svg" width="24" height="24"
                                viewBox="0 0 24 24" stroke-width="1.5" stroke="#ffffff" fill="none" stroke-linecap="round"
                                stroke-linejoin="round">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                                <circle cx="12" cy="12" r="9" />
                                <circle cx="12" cy="12" r="1" />
                                <path d="M7 12a5 5 0 0 1 5 -5" />
                                <path d="M12 17a5 5 0 0 0 5 -5" />
                            </svg>
                        {% endif %}
                        </div>
                        <div class="album-details-text">
                            <div class="album-details-album">{{ data['album'] }}</div>
                            <div class="album-details-artist">{{ data['album_artist'] }}</div>
                            <div class="album-details-more-details">
                                <span class="album-details-year">
                                    {{ data['year'] }}
                                </span>
                                <span class="bull">
                                    &bull;
                                </span>
                                <span class="album-details-track-total">
                                    {{ data['tracks']|length }} Tracks
                                </span>
                            </div>
                        </div>
                    </div>
                    <div id="album-details-track-list">
                        {% for track in data['tracks'] %}
                        <div class="album-details-track-item">
                            <div class="album-details-track-item-left">
                                <div class="album-details-track-item-number">{{ track['track'] }}</div>
                                <div class="album-details-track-item-title">{{ track['title'] }}</div>
                            </div>
                            <div class="album-details-track-item-duration">{{ track['formatted_duration'] }}</div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
    '''

    TRACKS = '''
        <div id="tracks-table-container">
                <table id="tracks-table">
                    {% for track in data %}
                    <tr class="tracks-table-row">
                        <td>
                            {% if track['image'] %}
                            <img class="tracks-table-row-cover" src="{{ track['image'] }}" alt="">
                            {% else %}
                            <svg xmlns="http://www.w3.org/2000/svg" class="tracks-table-row-cover tracks-table-row-svg"
                                width="24" height="24" viewBox="0 0 24 24" stroke-width="1.5" stroke="#ffffff"
                                fill="none" stroke-linecap="round" stroke-linejoin="round">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                                <circle cx="6" cy="17" r="3" />
                                <circle cx="16" cy="17" r="3" />
                                <polyline points="9 17 9 4 19 4 19 17" />
                                <line x1="9" y1="8" x2="19" y2="8" />
                            </svg>
                            {% endif %}
                        </td>
                        <td class="tracks-table-row-id">{{ track['id'] }}</td>
                        <td class="tracks-table-row-title">{{ track['title'] }}</td>
                        <td class="tracks-table-row-artist">{{ track['artist'] }}</td>
                        <td class="tracks-table-row-album">{{ track['album'] }}</td>
                        <td class="tracks-table-row-duration">{{ track['formatted_duration'] }}</td>
                    </tr>
                    {% endfor %}
                </table>
            </div>
    '''

    DEFAULT_VIEW = View.TRACKS

    def __init__(self) -> None:
        self.rendered_albums = None
        self.rendered_tracks = None
        pass

    
    def render(self, view, data):
        self.view = view
        if view == View.TRACKS:
            if self.rendered_tracks is None:
                self.rendered_tracks = Template(self.TRACKS).render(data=data)
            return self.rendered_tracks
        elif view == View.ALBUMS:
            if self.rendered_albums is None:
                self.rendered_albums = Template(self.ALBUMS).render(data=data)
            return self.rendered_albums
        elif view == View.ALBUM_DETAILS:
            return Template(self.ALBUM_DETAILS).render(data=data)
        

