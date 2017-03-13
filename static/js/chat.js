       $(document).ready(function(){
        var chatroomId = "chatroom" + {{=request.args[0]}}
        var log = $('#chatbox');
        log.animate({ scrollTop: log.prop('scrollHeight')}, 1000);
        var callback=function(e){
            $("#chatbox").load(location.href+" #chatbox >*","");
        };
      if(!$.web2py.web2py_websocket('ws://127.0.0.1:8888/realtime/' + chatroomId , callback))
         alert("html5 websocket not supported by your browser, try Google Chrome");
   });
  jQuery('#sendMessage').submit(function() {
  ajax("{{=URL('new_message')}}", ['your_message','room_id'], '');
  return false;
}); 