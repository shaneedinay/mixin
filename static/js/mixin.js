
$(document).ready( function () {

  $('#mi-create-music-room-button').on("click", function(){
    $('#mi-create-music-room-form').show();
  });
  $("#mi-create-music-room-close").on("click", function () {
    $('#mi-create-music-room-form').hide();
  });

  $(".mi-add-to-mr").on("click", function (){
    $("#mi-add-to-mr-form").show();
  });
  $("#mi-add-to-mr-close").on("click", function () {
    $("#mi-add-to-mr-form").hide();
  });

  $("#mi-search-music-input").on('keypress', function () {
    var key = (event.keyCode) ? event.keyCode : event.which;
    if(key == 13) { // Enter
			getSoundCloudResults();
		}
  });

  /* Start of Soundcloud API usage */

  // initialization
  $("#mi-search-soundcloud-api").click(function () {
      getSoundCloudResults(); //when the document loads the api functions will be ready
  });

  function getSoundCloudResults(){ //this is the function that holds the Soundcloud song player api
    if( $("#mi-search-results-player").length > 0 ) {
      $("#mi-search-results-player").remove();
      var new_result_div = document.createElement("div");
      $(new_result_div).attr("id", "mi-search-results-player");
      $("#mi-search-results").append(new_result_div);
    } else {
      var new_result_div = document.createElement("div");
      $(new_result_div).attr("id", "mi-search-results-player");
      $("#mi-search-results").append(new_result_div);
    }

    SC.initialize({ // this will initialize the client id needed for access to the SC api
        client_id: "M0gen3egUbJm4q7oXlWr8Dxt2Mr2ufCW"
    });

    // Play audio
    //---the soundcloud api call does not use ajax---it uses only javscript and there is an external script attatched in the index that adds more functionality
    var player = $("#SCplayer"); //the variable of SC player will be set to the id of the song media player
    var artist = $('#mi-search-music-input').val();  // the artist name will be defined as a string of text in the
    artist = artist.replace(/\s/g, "_");
    artist = artist.replace(".", "_");

    SC.get('/tracks', {
      q: artist,
    }).then(function(tracks) {
      if( tracks.length > 0) {
        $("#mi-search-results").css("display", "block");
      } else {
        $("#mi-search-results").css("display", "none");
      }
      console.log(tracks);
      $("#mi-music-room-info img").attr("src", tracks[0].artwork_url);
      console.log(tracks[0].permalink_url);

      // write to hidden value
      jQuery(".mi-search-results-add").on("click", function(){
        var cloudUrl = tracks[0].permalink_url;
        $("#mi-hidden-thisurl").val(cloudUrl);
        console.log(cloudUrl);
      });

      var num_tracks_load = tracks.length;
      if (num_tracks_load > 10) {
        num_tracks_load = 10;
      }
      for(var j = 0; j < num_tracks_load; j++) {
        var track_url = tracks[j].permalink_url;
        var thisID = "result" + j;
        var resultDiv = document.createElement("div");
        $(resultDiv).addClass("mi-search-results-song row");
        $(resultDiv).attr("id", thisID);
        $(resultDiv).html(function() {
          return '<div class="mi-search-results-song row">'
                 + '<div class="mi-search-results-left">'
              //   + '<a target="_blank" href="' + tracks[j].permalink_url + '">'
                 + '<button onclick="miSoundCloudAdd(addSC' + j + ')" id="addSC'+ j +'" title="'+ tracks[j].permalink_url +'" type="button" class="btn btn-sm btn-default mi-search-results-add">'
                 + '<span class="glyphicon glyphicon-plus"></span></button></div>'
                 + '<div class="mi-search-results-info">'
                 + '<p class="mi-search-results-title">' + tracks[j].title + '</p>'
                 + '<p class="mi-search-results-author">' + tracks[j].user.username + '</p>'
                 + '</div></div></div>';
        });

        $("#mi-search-results-player").append( $(resultDiv) );
      }
    });
  }
  /* End of Soundcloud API usage */

  /* Start of Youtube APU usage */
  $('#mi-search-youtube-api').on("click", function() {
    keyWordsearch();
  });

  function keyWordsearch() {
    gapi.client.setApiKey('AIzaSyA_blbHJ7KFigK782Fd0yfBBVbqxDWD5K4');
    gapi.client.load('youtube', 'v3', function() {
            makeRequest();
    });
  }

  function makeRequest() {
    if( $("#mi-search-results-player").length > 0 ) {
      $("#mi-search-results-player").remove();
      var new_result_div = document.createElement("div");
      $(new_result_div).attr("id", "mi-search-results-player");
      $("#mi-search-results").append(new_result_div);
    } else {
      var new_result_div = document.createElement("div");
      $(new_result_div).attr("id", "mi-search-results-player");
      $("#mi-search-results").append(new_result_div);
    }

    var q = $('#mi-search-music-input').val();
    var request = gapi.client.youtube.search.list({
            q: q,
            part: 'snippet',
            maxResults: 10
    });
    request.execute(function(response)
    {
      youtubeSongList = response.result.items;
      var srchItems = response.result.items;
      if( srchItems.length > 0) {
        $("#mi-search-results").css("display", "block");
      } else {
        $("#mi-search-results").css("display", "none");
      }
      var idx = 0;
      $.each(srchItems, function(index, item)  {
      idx = idx + 1;

      // var link = '<a target="_blank" href="'+item.id.videoId+'"><button class="btn btn-sm btn-default mi-serach-results-add" type="button"> <span class="glyphicon glyphicon-plus"></span></button></a>';
      // var info = '<p class="mi-search-results-title">' + item.snippet.title + '</p><p class="mi-search-results-author">' + item.snippet.channelTitle + '</p>';
      // var html = '<div id="result'+idx+'"class="mi-search-results-song row"><div class="mi-search-results-song row"><div class="mi-search-results-left">'+link+'</div><div class="mi-search-results-info">'+info+'</div></div></div>';

      var link = '<a target="_blank"><button class="btn btn-sm btn-default mi-serach-results-add" type="button"'+ "onclick='myYoutubeAdd(\""+item.id.videoId+"\")'>" +'<span class="glyphicon glyphicon-plus"></span></button></a>';
      var info = '<p class="mi-search-results-title">' + item.snippet.title + '</p><p class="mi-search-results-author">' + item.snippet.channelTitle + '</p>';
      var html = '<div id="result'+idx+'"class="mi-search-results-song row"><div class="mi-search-results-song row"><div class="mi-search-results-left">'+link+'</div><div class="mi-search-results-info">'+info+'</div></div></div>';

      $('#mi-search-results-player').append(html);
    })
  })
}
/* End of Youtube API Usage*/

});
