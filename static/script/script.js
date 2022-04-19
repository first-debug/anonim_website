function update_chat(){
$('#chat_box').empty();
$.getJSON( "/api/messages/" + chat_id, function( data ) {
 data.messages.forEach((element) => {
jQuery('<h4>', {
    class: 'message rounded bg-info w-25 container',
    text: element.message, element.type
}).appendTo('#chat_box');
})
});
}
setInterval(update_chat, 1000);