var musicroom-likes = 0;
var musicroom-dislikes = 0;
$(document).ready( function () {
  $("#mi-create-music-room-button").on("click", function () {
    alert("Button does not work yet");
  });

  $("#mi-music-room-like").on("click", function () {
    musicroom-likes++;
    $(mi-music-room-like-count).text(musicroom-likes);
    alert( "hello" );
  });
  $("#mi-music-room-dislike").on("click", function () {
    musicroom-dislikes++;
    $(mi-music-room-dislike-count).text(musicroom-dislikes);
  });
});
