from jinja2 import Template


def generate_album_template(data):
    html = '''
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

    template = Template(html)
    return template.render(data=data)

