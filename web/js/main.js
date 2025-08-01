const container = document.getElementById('container')
const tracks_table = document.getElementById('tracks-table');
const tracks_container = document.getElementById('tracks-table-container');
const albums_container = document.getElementById('albums-container');
const artists_container = document.getElementById('artists-container');
const favourites_container = document.getElementById('favourites-container');
const settings_container = document.getElementById('settings-container');
const playing_albumart = document.getElementById('playing-albumart');
const playing_albumart_svg = document.getElementById('playing-albumart-svg');
const playing_title = document.getElementById('playing-title');
const playing_artist = document.getElementById('playing-artist');
const btn_play_pause = document.getElementById('btn-play-pause');
const btn_next = document.getElementById('btn-next');
const btn_previous = document.getElementById('btn-previous');
const btn_shuffle = document.getElementById('btn-shuffle');
const btn_repeat = document.getElementById('btn-repeat');
const btn_settings = document.getElementById('settings');
const volume_slider = document.getElementById("volume-slider");
const seekbar = document.getElementById("seekbar");
const playing_time_total = document.getElementById('playing-time-total');
const playing_time_elapsed = document.getElementById('playing-time-elapsed');
const nav = document.getElementById('nav');
const nav_tracks = document.getElementById('nav-tracks');
const nav_albums = document.getElementById('nav-albums');
const nav_artists = document.getElementById('nav-artists');
const search_input = document.getElementById('search');
const style = getComputedStyle(document.body);

document.addEventListener('contextmenu', event => event.preventDefault());

var seekbar_track_color = style.getPropertyValue('--seekbar-track-color');
var seekbar_track_bg_color = style.getPropertyValue('--seekbar-track-background-color');
var volume_track_color = style.getPropertyValue('--seekbar-track-color');
var volume_track_bg_color = style.getPropertyValue('--seekbar-track-background-color');
var accent_color = style.getPropertyValue('--accent-color');

var selected_nav;
var active_container = albums_container;

btn_settings.addEventListener('click', function (e) {
    if (active_container != settings_container) {
        active_container.classList.toggle('inactive-container');
        settings_container.classList.toggle('inactive-container');
        active_container = settings_container;
        btn_settings.classList.toggle('settings-active');
        selected_nav.classList.toggle('selected-nav-item');
        selected_nav.getElementsByTagName('span')[0].classList.toggle('selected-indicator');
        selected_nav = null;
    }
});

const nav_items = nav.getElementsByClassName('nav-item');
var tracks_container_scroll = 0;
var albums_container_scroll = 0;
var artists_container_scroll = 0;
var favourites_container_scroll = 0;
var scroll_listener = null;
var tracks_container_search_input = "";
var albums_container_search_input = "";
var artists_container_search_input = "";
var favourites_container_search_input = "";

for (let i = 0; i < nav_items.length; i++) {
    const nav_item = nav_items[i];
    nav_item.addEventListener('click', function (e) {
        if (selected_nav != null) {
            selected_nav.classList.toggle('selected-nav-item');
            selected_nav.getElementsByTagName('span')[0].classList.toggle('selected-indicator');
        }
        selected_nav = this
        this.classList.toggle('selected-nav-item');
        this.getElementsByTagName('span')[0].classList.toggle('selected-indicator');
        if (active_container == settings_container) {
            btn_settings.classList.toggle('settings-active');
        }
        switch (this.textContent.trim()) {
            case "Tracks":
                if (active_container != tracks_container) {
                    search_input.value = null;
                    search_input.dispatchEvent(new Event('keyup'));
                    if (scroll_listener != null) {
                        container.removeEventListener('scroll', scroll_listener);
                    };
                    active_container.classList.toggle('inactive-container');
                    tracks_container.classList.toggle('inactive-container');
                    active_container = tracks_container;
                    container.scrollTop = tracks_container_scroll;
                    scroll_listener = function (e) {
                        tracks_container_scroll = container.scrollTop;
                    };
                    container.addEventListener('scroll', scroll_listener);
                }
                break;

            case "Albums":
                if (active_container != albums_container) {
                    search_input.value = null;
                    search_input.dispatchEvent(new Event('keyup'));
                    if (scroll_listener != null) {
                        container.removeEventListener('scroll', scroll_listener);
                    };
                    active_container.classList.toggle('inactive-container');
                    albums_container.classList.toggle('inactive-container');
                    active_container = albums_container;
                    container.scrollTop = albums_container_scroll;
                    scroll_listener = function (e) {
                        albums_container_scroll = container.scrollTop;
                    };
                    container.addEventListener('scroll', scroll_listener);
                }
                break;

            case "Artists":
                if (active_container != artists_container) {
                    search_input.value = null;
                    search_input.dispatchEvent(new Event('keyup'));
                    if (scroll_listener != null) {
                        container.removeEventListener('scroll', scroll_listener);
                    };
                    active_container.classList.toggle('inactive-container');
                    artists_container.classList.toggle('inactive-container');
                    active_container = artists_container;
                    container.scrollTop = artists_container_scroll;
                    scroll_listener = function (e) {
                        artists_container_scroll = container.scrollTop;
                    };
                    container.addEventListener('scroll', scroll_listener);
                }
                break;

            case "Favourites":
                if (active_container != favourites_container) {
                    search_input.value = null;
                    search_input.dispatchEvent(new Event('keyup'));
                    if (scroll_listener != null) {
                        container.removeEventListener('scroll', scroll_listener);
                    };
                    active_container.classList.toggle('inactive-container');
                    favourites_container.classList.toggle('inactive-container');
                    active_container = favourites_container;
                    container.scrollTop = favourites_container_scroll;
                    scroll_listener = function (e) {
                        favourites_container_scroll = container.scrollTop;
                    };
                    container.addEventListener('scroll', scroll_listener);
                }
                break;

            default:
                break;
        }
        selected_nav = this;
    });
    if (nav_item.classList.contains('selected-nav-item')) {
        selected_nav = nav_item;
    }
}


document.onkeypress = (e) => {
    if (e.code === 'Space') {
        if (document.activeElement.id != 'search') {
            e.preventDefault();
            eel.play_pause();
        }
    }
}


eel.get_volume()((volume) => {
    volume_slider.value = volume
    volume_slider.style.background = `linear-gradient(to right, ${volume_track_color} 0%, ${volume_track_color}  ${volume}%, ${volume_track_bg_color} ${volume}%, ${volume_track_bg_color} 100%)`;
});

eel.get_playing_metadata()((data) => {
    if (data) {
        set_playing_metadata(data);
    }
});

eel.is_playing()((result) => {
    set_playPause(result);
});


seekbar.style.background = `linear-gradient(to right, ${seekbar_track_color} 0%, ${seekbar_track_color}  0%, ${seekbar_track_bg_color} 0%, ${seekbar_track_bg_color} 100%)`;

seekbar.onmouseover = function () {
    seekbar_track_color = style.getPropertyValue('--seekbar-track-hover-color');
    var value = (this.value - this.min) / (this.max - this.min) * 100;
    this.style.background = `linear-gradient(to right, ${seekbar_track_color} 0%, ${seekbar_track_color}  ${value}%, ${seekbar_track_bg_color} ${value}%, ${seekbar_track_bg_color} 100%)`;
}

seekbar.onmouseout = function () {
    seekbar_track_color = style.getPropertyValue('--seekbar-track-color');
    var value = (this.value - this.min) / (this.max - this.min) * 100;
    this.style.background = `linear-gradient(to right, ${seekbar_track_color} 0%, ${seekbar_track_color}  ${value}%, ${seekbar_track_bg_color} ${value}%, ${seekbar_track_bg_color} 100%)`;
}


seekbar.oninput = function () {
    var duration = this.value;
    var value = (this.value - this.min) / (this.max - this.min) * 100;
    this.style.background = `linear-gradient(to right, ${seekbar_track_color} 0%, ${seekbar_track_color}  ${value}%, ${seekbar_track_bg_color} ${value}%, ${seekbar_track_bg_color} 100%)`;
    if (duration != 0) {
        playing_time_elapsed.textContent = duration_to_str(duration - 1);
    } else {
        playing_time_elapsed.textContent = duration_to_str(0);
    }
    eel.seek_to(value);
};


volume_slider.onmouseover = function () {
    volume_track_color = style.getPropertyValue('--seekbar-track-hover-color');
    var value = this.value;
    this.style.background = `linear-gradient(to right, ${volume_track_color} 0%, ${volume_track_color}  ${value}%, ${volume_track_bg_color} ${value}%, ${volume_track_bg_color} 100%)`;
}

volume_slider.onmouseout = function () {
    volume_track_color = style.getPropertyValue('--seekbar-track-color');
    var value = this.value;
    this.style.background = `linear-gradient(to right, ${volume_track_color} 0%, ${volume_track_color}  ${value}%, ${volume_track_bg_color} ${value}%, ${volume_track_bg_color} 100%)`;
}


volume_slider.oninput = function () {
    var value = this.value;
    this.style.background = `linear-gradient(to right, ${volume_track_color} 0%, ${volume_track_color}  ${value}%, ${volume_track_bg_color} ${value}%, ${volume_track_bg_color} 100%)`;
    eel.set_volume(value);
};


eel.expose(audio_complete);
function audio_complete() {
    eel.complete();
}

eel.expose(update_seekbar)
function update_seekbar(duration) {
    playing_time_elapsed.textContent = duration_to_str(duration);
    seekbar.value = duration;
    var value = (seekbar.value - seekbar.min) / (seekbar.max - seekbar.min) * 100
    seekbar.style.background = `linear-gradient(to right, ${seekbar_track_color} 0%, ${seekbar_track_color}  ${value}%, ${seekbar_track_bg_color} ${value}%, ${seekbar_track_bg_color} 100%)`;
};


btn_play_pause.addEventListener('click', () => {
    eel.play_pause();
});

btn_next.addEventListener('click', () => {
    eel.next_track();
});

btn_previous.addEventListener('click', () => {
    eel.previous_track();
});

const tracks_list = tracks_table.getElementsByClassName('tracks-table-row');
for (let i = 0; i < tracks_list.length; i++) {
    const track = tracks_list[i];
    track.addEventListener("click", function (e) {
        eel.play_track(parseInt(this.getElementsByClassName('tracks-table-row-id')[0].textContent) - 1);
    });
}

const albums_list = albums_container.getElementsByClassName('albums-container-item');
for (let i = 0; i < albums_list.length; i++) {
    const album = albums_list[i];
    album.addEventListener("click", function (e) {
        let album_name = this.getElementsByClassName('albums-container-item-album')[0].textContent;
        nav_tracks.click();
        search_input.value = `$album:${album_name}`;
        search_input.dispatchEvent(new Event('keyup'));
    });
}

const artists_list = artists_container.getElementsByClassName('artists-container-item');
for (let i = 0; i < artists_list.length; i++) {
    const artist = artists_list[i];
    artist.addEventListener("click", function (e) {
        let artist_name = this.getElementsByClassName('artists-container-item-artist')[0].textContent;
        nav_albums.click();
        search_input.value = `$artist:${artist_name}`;
        search_input.dispatchEvent(new Event('keyup'));
    });
}

eel.expose(set_playing_metadata);

function set_playing_metadata(data) {
    if (data.image != null) {
        playing_albumart.style.display = "block";
        playing_albumart_svg.style.display = "none";
        playing_albumart.setAttribute(
            'src', data.image
        );
        document.documentElement.style.backgroundImage = `url('${data.image}')`;
        document.documentElement.style.backgroundSize = 'cover';
    } else {
        playing_albumart.style.display = "none";
        playing_albumart_svg.style.display = "block";
        document.documentElement.style.background = style.getPropertyValue('--html-background-gradient');
    }
    playing_artist.textContent = data.artist;
    playing_title.textContent = data.title;
    playing_time_total.textContent = duration_to_str(data.duration);
    playing_time_elapsed.textContent = duration_to_str(0);
    seekbar.max = data.duration;
    seekbar.value = 0;
    seekbar.style.background = 'linear-gradient(to right, #b3b3b3 0%, #b3b3b3 ' + 0 + '%, #505050 ' + 0 + '%, #505050 100%)';
}

function clear_playing_metadata() {
    playing_albumart.setAttribute(
        'src', './icons/music.svg'
    );
    playing_artist.textContent = 'Not Playing';
    playing_title.textContent = 'Not Playing';
}

eel.expose(set_playPause);

function set_playPause(is_playing) {
    if (is_playing) {
        btn_play_pause.setAttribute(
            'src', '../icons/pause.svg'
        );
    }
    else {
        btn_play_pause.setAttribute(
            'src', '../icons/play.svg'
        );
    }
}

function duration_to_str(duration) {
    var mins = ~~(duration / 60);
    var secs = ~~duration % 60;
    return (mins < 10 ? "0" : "") + mins + ":" + (secs < 10 ? "0" : "") + secs;
}


function visualizer() {
    return
}


function searchTrack() {
    var input, filter, filter_by, list, items, title_element, artist_element, album_element, albums_items, album_view_album, album_view_artist;
    input = document.getElementById('search');
    filter = input.value;
    filter_by = [];

    if (filter.indexOf("$album:") > -1) {
        filter = filter.slice(7);
        filter_by.push('album');
    }
    if (filter.indexOf("$artist:") > -1) {
        filter = filter.slice(8);
        filter_by.push('artist');
    }
    filter = filter.toUpperCase();
    list = document.getElementById("tracks-table");
    items = list.getElementsByClassName('tracks-table-row');

    for (let i = 0; i < items.length; i++) {
        title_element = items[i].getElementsByClassName("tracks-table-row-title")[0];
        artist_element = items[i].getElementsByClassName("tracks-table-row-artist")[0];
        album_element = items[i].getElementsByClassName("tracks-table-row-album")[0];

        let title = title_element.textContent || title_element.innerText;
        let artist = artist_element.textContent || artist_element.innerText;
        let album = album_element.textContent || album_element.innerText;

        if ((title.toUpperCase().indexOf(filter) > -1) ||
            (artist.toUpperCase().indexOf(filter) > -1) ||
            (album.toUpperCase().indexOf(filter) > -1)) {
            items[i].style.display = "";
        } else {
            items[i].style.display = "none";
        }
    }

    for (let i = 0; i < albums_list.length; i++) {
        const album = albums_list[i];

        let album_name = album.getElementsByClassName(
            'albums-container-item-album')[0].textContent;
        let album_artist = album.getElementsByClassName(
            'albums-container-item-artist')[0].textContent;

        if ((album_name.toUpperCase().indexOf(filter) > -1) ||
            (album_artist.toUpperCase().indexOf(filter) > -1)) {
            album.style.display = "";
        } else {
            album.style.display = "none";
        }
    }
}


const reorder = () => {
    const frag = document.createDocumentFragment();
    const list = document.getElementById("tracks-table");
    const items = list.getElementsByClassName('tracks-table-row');
    const sortedList = [...items].sort((a, b) => {
        const c = a.getElementsByClassName("tracks-table-row-album")[0].textContent,
            d = b.getElementsByClassName("tracks-table-row-album")[0].textContent;
        return c < d ? -1 : c > d ? 1 : 0;
    });
    for (const item of sortedList) {
        frag.appendChild(item);
    }
    list.appendChild(frag);
}

reorder();

var repeat = 0;

const repeat_all_none = btn_repeat.getElementsByClassName('repeat-all-none')[0];
const repeat_one = btn_repeat.getElementsByClassName('repeat-one')[0];
const repeat_icon_color = style.getPropertyValue('--player-primary-icon-color');

eel.get_repeat_state()((repeat) => {
    set_repeat(repeat);
});

btn_repeat.addEventListener('click', function (e) {

    if (repeat == 2) {
        repeat = 0
    } else {
        repeat++;
    }

    set_repeat(repeat);
    eel.set_repeat_state(repeat);
});

function set_repeat(repeat) {
    switch (repeat) {
        case 0:
            repeat_all_none.style.display = "block"
            btn_repeat.style.fill = repeat_icon_color;
            repeat_one.style.display = "none";
            break;

        case 1:
            btn_repeat.style.fill = accent_color;
            break;

        case 2:
            btn_repeat.style.fill = accent_color;
            repeat_all_none.style.display = "none";
            repeat_one.style.display = "block";
            break;

        default:
            break;
    }
}



{/* // `<div class="tracks-container-item">
    //                 <div class="tracks-container-item-left">
    //                     <p class="tracks-container-item-number">${index}</p>
    //                     <img class="tracks-container-item-img" src="icons/music.svg" alt="">
    //                     <p class="tracks-container-item-name">Unknown Title</p>
    //                 </div>
    //                 <div class="tracks-container-item-text">Unknown Artist</div>
    //                 <div class="tracks-container-item-text">Unknown Album</div>
    //                 <div class="tracks-container-item-text text-align-end">--:--</div>
    //             </div>` */};


nav_tracks.click();

function dive() {
    var height = container.scrollHeight;
    for (let index = 0; index < height; index++) {
        container.scrollTop(index)
    }
}

class Container{

    constructor(container, nav = null) {
        this.container = container;
        this.nav = nav;
    }

    active() {
        search_input.value = null;
        search_input.dispatchEvent(new Event("keyup"));
        if (scroll_listener != null) {
          container.removeEventListener("scroll", scroll_listener);
        }
        active_container.classList.toggle("inactive-container");
        tracks_container.classList.toggle("inactive-container");
        active_container = tracks_container;
        container.scrollTop = tracks_container_scroll;
        scroll_listener = function (e) {
          tracks_container_scroll = container.scrollTop;
        };
        container.addEventListener("scroll", scroll_listener);
    }

}
