
var musicroom_likes = 0;
var musicroom_dislikes = 0;
$(document).ready( function () {
  $("#mi-create-music-room-button").on("click", function () {
    alert("Button does not work yet");
  });

  $("#mi-music-room-like").on("click", function () {
    musicroom_likes++;
    $("#mi-music-room-like-count").text(musicroom_likes);
  });

  $("#mi-music-room-dislike").on("click", function () {
    musicroom_dislikes++;
    $("#mi-music-room-dislike-count").text(musicroom_dislikes);
  });

});
