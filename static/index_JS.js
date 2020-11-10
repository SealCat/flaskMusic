//数组下标
index = -1;

var lineNo = 0;
var fraction = 0.5;
var topNum = 0;


function lineHeight(lineno) {
    var ul = $("#text");
    var $ul = document.getElementById('text');
    // 令正在唱的那一行高亮显示
    if (lineno > 0) {
        $(ul.find("li").get(topNum + lineno - 1)).removeClass("lineheight");
    }
    var nowline = ul.find("li").get(topNum + lineno);
    $(nowline).addClass("lineheight");

    // 实现文字滚动
    var _scrollTop;
    $ul.scrollTop = 0;
    if ($ul.clientHeight * fraction > nowline.offsetTop) {
        _scrollTop = 0;
    } else if (nowline.offsetTop > ($ul.scrollHeight - $ul.clientHeight * (1 - fraction))) {
        _scrollTop = $ul.scrollHeight - $ul.clientHeight;
    } else {
        _scrollTop = nowline.offsetTop - $ul.clientHeight * fraction;
    }

    //以下声明歌词高亮行固定的基准线位置成为 “A”
    if ((nowline.offsetTop - $ul.scrollTop) >= $ul.clientHeight * fraction) {
        //如果高亮显示的歌词在A下面，那就将滚动条向下滚动，滚动距离为 当前高亮行距离顶部的距离-滚动条已经卷起的高度-A到可视窗口的距离
        $ul.scrollTop += Math.ceil(nowline.offsetTop - $ul.scrollTop - $ul.clientHeight * fraction);

    } else if ((nowline.offsetTop - $ul.scrollTop) < $ul.clientHeight * fraction && _scrollTop != 0) {
        //如果高亮显示的歌词在A上面，那就将滚动条向上滚动，滚动距离为 A到可视窗口的距离-当前高亮行距离顶部的距离-滚动条已经卷起的高度
        $ul.scrollTop -= Math.ceil($ul.clientHeight * fraction - (nowline.offsetTop - $ul.scrollTop));

    } else if (_scrollTop == 0) {
        $ul.scrollTop = 0;
    } else {
        $ul.scrollTop += $(ul.find('li').get(0)).height();
    }
}


//创建音乐列表
function createBox() {
    var html = "";
    for (var i = 0; i < myMusics.length; i++) {
        html += "<li>" + (i + 1) + "  <a href='javascript:clickName(" + i + ");'>" + myMusics[i].title + "</a></li>"
    }
    return html
}
//点击名字播放音乐
function clickName(i) {
    index = i;
    playMusic(0);
}

function stopmusic() { //按钮"播放/暂停"单击事件
	var bt = document.getElementById("playMusic")
	if (bt.value == "播放") {
		bt.value="暂停";
		document.getElementById("media").play();
	} else if (bt.value == "暂停") {
		bt.value="播放";
		document.getElementById("media").pause();
	}
}
//音乐播放
function playMusic(s) {
    $("#playMusic").val("暂停");
    if (s == 0) { //点击名字播放音乐

    } else if (s == 1) { //下一首
        $("#playMusic").val("暂停");
		index++;
        if (index >= myMusics.length) {
            index = 0;
        }
	}
    
    //修改audio资源路径
    $("#media").attr("src", myMusics[index].src);
    //音乐播放
    $("#media").play;
    //显示音乐名称
    $("#musicTitle").text(myMusics[index].title);
    $("title").text(myMusics[index].title);
    //重置li列表背景色
    $("#box").children("li").css("background-color", "rgba(255,255,255,0)");

    //修改播放音乐背景色
    $($("#box").children("li")[index]).css("background-color", "rgba(240,240,240,0.5)");
    $($("#box").children("li")[index]).css("font-weight", "bold");
    $("#sliding").offset({
        left: 60
    });
	
	document.getElementById("text").innerHTML = "";
	lineNo = 0
	$.ajax({
		url: "/lrc",
		dataType: "json",
		async: true,
		data: {
			"target": myMusics[index].src
		},
		type: "POST",
		success: function(req) {
			medisArray = req;
			var ul = $("#text");
			// 遍历medisArray，并且生成li标签，将数组内的文字放入li标签
			$.each(medisArray, function(i, item) {
				var li = $("<li style='list-style: none;'>");
				li.html(item.c);
				ul.append(li);
			});
		},
		error: function(e) {
			var medis = e.responseText;
			var medises = medis.split("\n"); // 用换行符拆分获取到的歌词

			$.each(medises, function(i, item) { // 遍历medises，并且将时间和文字拆分开，并push进自己定义的数组，形成一个对象数组
				var t = item.substring(item.indexOf("[") + 1, item.indexOf("]"));
				medisArray.push({

					t: (t.split(":")[0] * 60 + parseFloat(t.split(":")[1])).toFixed(3),
					c: item.substring(item.indexOf("]") + 1, item.length)
				});
			});
			var ul = $("#text");
			// 遍历medisArray，并且生成li标签，将数组内的文字放入li标签
			$.each(medisArray, function(i, item) {
				var li = $("<li style='list-style: none;'>");
				li.html(item.c);
				ul.append(li);
			});
		}
	});
}


//时间获取
function timeupdate() {
    //获取audio元素
    var media = document.getElementById("media");
    //音乐当前位置
    var curr = Math.floor(media.currentTime);
    //音乐长度
    var dur = Math.floor(media.duration);
    $("#totalTime").text("时长：" + formatTime(dur));
    $("#currTime").text("当前：" + formatTime(curr));
	if (lineNo == medisArray.length - 1 && media.currentTime.toFixed(3) >= parseFloat(medisArray[lineNo].t)) {
        lineHeight(lineNo);
    }
    if (parseFloat(medisArray[lineNo].t) <= media.currentTime.toFixed(3) &&
        media.currentTime.toFixed(3) <= parseFloat(medisArray[lineNo + 1].t)) {
        lineHeight(lineNo);
        lineNo++;
    }
}
//音乐计时格式
function formatTime(time) {
    var h = 0,
        i = 0,
        s = parseInt(time);
    if (s > 60) {
        i = parseInt(s / 60);
        s = parseInt(s % 60);
        if (i > 60) {
            h = parseInt(i / 60);
            i = parseInt(i % 60);
        }
    }
    var zero = function(v) {
        return (v >> 0) < 10 ? "0" + v : v;
    };
    return (zero(h) + ":" + zero(i) + ":" + zero(s));
};

function button_click() {
    $.ajax({
        url: "/find",
        dataType: "json",
        async: true,
        data: {
            "target": document.getElementById("nn").value
        },
        type: "POST",
        success: function(req) {
            myMusics = req;
            //页面加载
            $(document).ready(function() {
                //$("#" + "box").append(createBox());
                document.getElementById("box").innerHTML=createBox();
                playMusic(1);
            });
        },
        error: function(e) {
            alert(e)
        }
    });
}

function clickM(tarK,T) {
    document.getElementById("Title").innerHTML=T;
    $.ajax({
        url: "/music",
        dataType: "json",
        async: true,
        data: {
            "target": tarK
        },
        type: "POST",
        success: function(req) {

            myMusics = req;
            var html = "";
            for (var i = 0; i < req.length; i++) {
                html += "<li>" + (i + 1) + "  <a href='javascript:clickName(" + i + ");'>" + req[i].title + "</a></li>"
            }
            //页面加载
            $(document).ready(function() {
                document.getElementById("box").innerHTML=html;
                playMusic(1);
            });
        },
        error: function(e) {
            alert(e)
        }
    });
}
