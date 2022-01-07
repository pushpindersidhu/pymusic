const tracks_table = document.getElementById('tracks-table');
const tracks_container = document.getElementById('tracks-table-container');
const albums_container = document.getElementById('albums-container');
const playing_albumart = document.getElementById('playing-albumart');
const playing_title = document.getElementById('playing-title');
const playing_artist = document.getElementById('playing-artist');
const btn_play_pause = document.getElementById('btn-play-pause');
const btn_next = document.getElementById('btn-next');
const btn_previous = document.getElementById('btn-previous');
const volume_slider = document.getElementById("volume-slider");
const seekbar = document.getElementById("seekbar");
const playing_time_total = document.getElementById('playing-time-total');
const playing_time_elapsed = document.getElementById('playing-time-elapsed');
const nav = document.getElementById('nav');
const nav_tracks = document.getElementById('nav-tracks');
const nav_albums = document.getElementById('nav-albums');
const style = getComputedStyle(document.body);

document.addEventListener('contextmenu', event => event.preventDefault());

var seekbar_track_color = style.getPropertyValue('--seekbar-track-color');
var seekbar_track_bg_color = style.getPropertyValue('--seekbar-track-background-color');
var volume_track_color = style.getPropertyValue('--seekbar-track-color');
var volume_track_bg_color = style.getPropertyValue('--seekbar-track-background-color');


var selected_nav;
var active_container = albums_container;

const nav_items = nav.getElementsByClassName('nav-item');
console.log(nav_items);
for (let i = 0; i < nav_items.length; i++) {
    const nav_item = nav_items[i];
    nav_item.addEventListener('click', function (e) {
        if (selected_nav == this) {
            return;
        }
        selected_nav.classList.remove('selected-nav-item');
        selected_nav.getElementsByTagName('span')[0].classList.remove('selected-indicator');
        this.classList.add('selected-nav-item');
        this.getElementsByTagName('span')[0].classList.add('selected-indicator');
        console.log(this.textContent.trim());
        switch (this.textContent.trim()) {
            case "Tracks":
                if (active_container != tracks_container) {
                    active_container.classList.toggle('inactive-container');
                    tracks_container.classList.toggle('inactive-container');
                    active_container = tracks_container;
                }
                break;

            case "Albums":
                if (active_container != albums_container) {
                    active_container.classList.toggle('inactive-container');
                    albums_container.classList.toggle('inactive-container');
                    active_container = albums_container;
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
        e.preventDefault();
        eel.play_pause()(() => {
            set_playPause();
        });
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
    playing_time_elapsed.textContent = duration_to_str(duration);
    eel.seek_to(duration);
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
    window.clearInterval(seekbar_updater);
    eel.complete();
}

function update_seekbar() {
    eel.get_duration()((duration) => {
        playing_time_elapsed.textContent = duration_to_str(duration);
        seekbar.value = duration;
        var value = (seekbar.value - seekbar.min) / (seekbar.max - seekbar.min) * 100
        seekbar.style.background = `linear-gradient(to right, ${seekbar_track_color} 0%, ${seekbar_track_color}  ${value}%, ${seekbar_track_bg_color} ${value}%, ${seekbar_track_bg_color} 100%)`;
    });
};

var seekbar_updater;

eel.get_playing_metadata()((data) => {
    if (data) {
        set_playing_metadata(data);
    }
});

btn_play_pause.addEventListener('click', () => {
    eel.play_pause()(() => {
        set_playPause();
    });
});

btn_next.addEventListener('click', () => {
    eel.next_track()(() => {
        eel.get_playing_metadata()((data) => {
            set_playing_metadata(data);
        });
    });
});

btn_previous.addEventListener('click', () => {
    eel.previous_track()(() => {
        eel.get_playing_metadata()((data) => {
            set_playing_metadata(data);
        });
    });
});

const tracks_list = tracks_table.getElementsByClassName('tracks-table-row');
for (let i = 0; i < tracks_list.length; i++) {
    const track = tracks_list[i];
    track.addEventListener("click", function (e) {
        eel.play_track(parseInt(this.getElementsByClassName('tracks-table-row-id')[0].textContent) - 1)((result) => {
            if (result) {
                window.clearInterval(seekbar_updater);
                seekbar_updater = window.setInterval(update_seekbar, 1000);
                eel.get_playing_metadata()((data) => {
                    set_playing_metadata(data);
                });
            } else {
                window.clearInterval(seekbar_updater);
                clear_playing_metadata();
            }
        });
    });
}

eel.expose(set_playing_metadata);

function set_playing_metadata(data) {
    playing_albumart.setAttribute(
        'src', data.image
    );
    playing_artist.textContent = data.artist;
    playing_title.textContent = data.title;
    playing_time_total.textContent = duration_to_str(data.duration);
    playing_time_elapsed.textContent = duration_to_str(0);
    seekbar.max = data.duration;
    seekbar.value = 0;
    seekbar.style.background = 'linear-gradient(to right, #b3b3b3 0%, #b3b3b3 ' + 0 + '%, #505050 ' + 0 + '%, #505050 100%)';
    set_playPause();
}

function clear_playing_metadata() {
    playing_albumart.setAttribute(
        'src', './icons/music.svg'
    );
    playing_artist.textContent = 'Not Playing';
    playing_title.textContent = 'Not Playing';
}

eel.expose(set_playPause);

function set_playPause() {
    update_seekbar();
    eel.is_playing()((result) => {
        if (result) {
            window.clearInterval(seekbar_updater);
            seekbar_updater = window.setInterval(update_seekbar, 1000);
            btn_play_pause.setAttribute(
                'src', '../icons/pause.svg'
            );
        }
        else {
            btn_play_pause.setAttribute(
                'src', '../icons/play.svg'
            );
            window.clearInterval(seekbar_updater);
        }
    });
}

function duration_to_str(duration) {
    var mins = ~~(duration / 60);
    var secs = ~~duration % 60;
    return (mins < 10 ? "0" : "") + mins + ":" + (secs < 10 ? "0" : "") + secs;
}


function visualizer() {
    return
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
