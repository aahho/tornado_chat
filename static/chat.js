var ws;
        Zepto(function($){
            init_ws();

            window.onbeforeunload = function(e) {
                ws.close()
            };

        })

        function init_ws() {
                var url;
                url = "ws://"+window.location.host  + "/ws/"+client_id +"/"+ channel_id;
                ws = new WebSocket( url );
                ws.onopen  = function(event) {
                    console.log("Socket opened");
                    init_chat_ui();
                }

                ws.onclose = function(){
                    console.log("WebSocket closed.");
                }

                ws.onerror  = function(event) {
                    console.log("ERROR opening WebSocket.");
                    $('body').html("<h1>ERROR connecting to chat server</h1><p>reload the page and try again</p>");
                }

                ws.onmessage = receive_message;

            };

            function init_chat_ui() {
                $("#txtMsg").keyup(function(event) {
                        if ( $(this).val() != "") {
                            $("#btnSend").removeAttr("disabled");
                            //if key is enter, send message and clean box
                            if (event.which == 13) {
                                send_text_msg($("#txtMsg").val());
                                $("#btnSend").attr("disabled", "disabled");
                            }
                        } else {
                            $("#btnSend").attr("disabled", "disabled");
                        }
                });
                $("#btnSend").click(function() {
                    send_text_msg($("#txtMsg").val())
                    $("#btnSend").attr("disabled", "disabled");
                });
                $("#chat").show(400);
                }

            function send_text_msg(txt) {
                text_msg_obj = {"msgtype": "text", "payload": txt };
                $("#txtMsg").val("");
                $("#txtMsg").focus();
                jmsg = JSON.stringify(text_msg_obj );
                ws.send(jmsg);
            };

            function receive_message(wsevent) {
                console.log("received message: "+wsevent.data )
                msg_obj = $.parseJSON(wsevent.data);
                switch (msg_obj.message.type) {
                    case "join": $("#msgList").append("<div class='col-12 row' style='margin-top: 10px;'><div class='col-3' style='padding: 0px;text-align: left;'> <span style='padding: 2px 7px;background: #1ea3e2;border-radius: 50%;margin-left: 10px;color: #fff;'>"+msg_obj.user.username.charAt(0).toUpperCase()+"</span><span style='text-align:left;padding: 2px 0px 0px 7px;'><b>"+msg_obj.user.username.charAt(0).toUpperCase()+msg_obj.user.username.slice(1)+"</b> </span></div><div class=col-9 style='text-align:left;padding: 2px 0px 0px 7px;'> "+ msg_obj.message.payload + "</div></div>");
                    break;
                    case "leave":$("#msgList").append("<div class='col-12 row' style='margin-top: 10px;'><div class='col-3' style='padding: 0px;text-align: left;'> <span style='padding: 2px 7px;background: #1ea3e2;border-radius: 50%;margin-left: 10px;color: #fff;'>"+msg_obj.user.username.charAt(0).toUpperCase()+"</span><span style='text-align:left;padding: 2px 0px 0px 7px;'><b>"+msg_obj.user.username.charAt(0).toUpperCase()+msg_obj.user.username.slice(1)+"</b> </span></div><div class=col-9 style='text-align:left;padding: 2px 0px 0px 7px;'> "+ msg_obj.message.payload + "</div></div>");
                                  break;
                    case "connected_users": $("#nickList").empty()
                                      $("#nickList").append("<ul>");
                                      nl = _.map(msg_obj.payload, function(nick){ return "<li>"+nick+"</li>"; })
                                      ih =  _.reduce(nl, function(inner, li){ return inner + '\n'+ li; }, "");
                                      $("#nickList").append(ih);
                                      $("#nickList").append("</ul>");
                                  break;
                    default: $("#msgList").append("<div class='col-12 row' style='margin-top: 10px;'><div class='col-3' style='padding: 0px;text-align: left;'> <span style='padding: 2px 7px;background: #1ea3e2;border-radius: 50%;margin-left: 10px;color: #fff;'>"+msg_obj.user.username.charAt(0).toUpperCase()+"</span><span style='text-align:left;padding: 2px 0px 0px 7px;'><b>"+msg_obj.user.username.charAt(0).toUpperCase()+msg_obj.user.username.slice(1)+"</b> </span></div><div class=col-9 style='text-align:left;padding: 2px 0px 0px 7px;'> "+ msg_obj.message.payload + "</div></div>");
                }

                $("#msgList").scrollTop($("#msgList")[0].scrollHeight);
            }