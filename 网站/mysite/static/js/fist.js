const websocket = new WebSocket("ws://192.168.124.89:8000/message/");
//是否暂停
let flag_pause = 0
//自动检测
let auto_detect = 0
// 监听 WebSocket 连接打开事件
websocket.onopen = function () {
    console.log("WebSocket connect is opening");
};

// 监听 WebSocket 消息接收事件
websocket.onmessage = function (event) {
    function updateImage(imageId, imageData) {
        // Decode the Base64 encoded image data
        const imageDataBytes = new Uint8Array(atob(imageData).length);
        const decodedData = atob(imageData);

// Use a loop with faster character code access
        for (let i = 0; i < imageDataBytes.length; i++) {
            imageDataBytes[i] = decodedData.charCodeAt(i);
        }

        // Create a Blob object with the image data
        const blob = new Blob([imageDataBytes], {type: 'image/png'});

        // Create an Image object and set its src as data URL
        const image = new Image();
        image.onload = function () {
            // Update the image element in HTML
            document.getElementById(imageId).src = image.src;
        };
        image.onerror = function () {
            console.error("Failed to load image for", imageId);
        };
        image.src = URL.createObjectURL(blob);
    }

    let data = JSON.parse(event.data);
// Assuming data is already a parsed JSON object
    let flag = 0;
    if (auto_detect) {
        flag = data.flag;
    } else {
        flag = 0;
    }
    const image0Data = data.image0;

    updateImage('image0', image0Data);
    //console.log("更新图片", image.src);
    // 检测到破损
    var popup = document.getElementById("popup");
    if (flag) {
        const image1Data = data.image1;
        console.log('yes, it resizeing');
        updateImage('image1', image1Data);
        // 显示弹出框
        //弹框
        var rejectButton = document.getElementById("reject");
        var agreeButton = document.getElementById("agree");
        if (popup.style.display !== "block") {
            popup.style.display = "block";

            function CountDown() {
                // 开始倒计时
                var countdown = 5;
                var interval = setInterval(function () {
                    countdown--;
                    if (countdown === 0) {
                        // 倒计时结束
                        clearInterval(interval);
                        // 关闭弹出框
                        popup.style.display = "none";
                    } else {
                        agreeButton.textContent = "同意(" + countdown + "s)";
                    }
                }, 1000);
            }

            CountDown()
            agreeButton.addEventListener("click", function () {
                // 同意上报
                // 关闭弹出框
                popup.style.display = "none";
                websocket.send(JSON.stringify({
                    "command": "con"
                }));
            });
            rejectButton.addEventListener("click", function () {
                // 拒绝上报
                // 关闭弹出框
                popup.style.display = "none";
                if (auto_detect) {
                    websocket.send(JSON.stringify({
                        "command": "con"
                    }));
                }
            });
        }
    } else {
        document.getElementById('image1').src = '/static' + '/img/logo.png';
    }
    if (popup.style.display !== "block") {
        // 弹出框已消失，执行后续代码
        //发送确认帧
        //自动检测
        if (auto_detect) {
            if (flag_pause - 1) {
                websocket.send(JSON.stringify({
                    "command": "con"
                }));
                console.log('收到');
            }
        }
    }
};

// 监听按钮点击"开始自动"按钮事件
document.getElementById("btnStart").addEventListener("click", function () {
    flag_pause = 0;
    auto_detect = 1;
    // 发送指令给消费者
    const box = document.getElementById("btnStart");
    box.style.backgroundColor = "red";
    const box1 = document.getElementById("btnStop");
    box1.style.backgroundColor = "black";
    websocket.send(JSON.stringify({
        "command": "start"
    }));
});
// 监听按钮点击"开始人工"按钮事件
document.getElementById("btnStart_hum").addEventListener("click", function () {
    flag_pause = 0
    // 发送指令给消费者
    const box = document.getElementById("btnStart_hum");
    box.style.backgroundColor = "red";
    const box1 = document.getElementById("btnStop");
    box1.style.backgroundColor = "black";
    //开启方向
    const pop = document.getElementById("direction-big");
    pop.style.display = "block";
    pop.style.top = "10%";
    pop.style.left = "50%"; // 水平居中定位
    pop.style.transform = "translateX(-50%)"; // 使容器居中
    websocket.send(JSON.stringify({
        "command": "start"
    }));
});

//人工检测方向监听
const buttonForward = document.getElementById("buttonForward");
const buttonBackward = document.getElementById("buttonBackward");

// 定时器变量，用于持续执行的操作
let intervalId = null;

// 持续执行的操作函数
function performAction(button) {
    if (button.id === "buttonForward") {
        websocket.send(JSON.stringify({
            "command": "conF"
        }));
    } else {
        websocket.send(JSON.stringify({
            "command": "conB"
        }));
    }

}

// 按钮按下事件处理程序
function onPressStart(event) {
    event.preventDefault(); // 阻止浏览器默认行为
    const button = event.target;
    // 持续执行操作
    intervalId = setInterval(() => performAction(button), 100); // 每100ms执行一次
    // 返回 true
    return true;
}

// 按钮松开事件处理程序
function onPressEnd() {
    // 停止持续执行的操作
    clearInterval(intervalId);
    console.log('yes,triger,end');
    intervalId = null;
    // 返回 false
    return false;
}

// 为按钮添加事件监听
buttonForward.addEventListener("mousedown", onPressStart);
buttonForward.addEventListener("mouseup", onPressEnd);
buttonForward.addEventListener("touchstart", onPressStart);
buttonForward.addEventListener("touchend", onPressEnd);

buttonBackward.addEventListener("mousedown", onPressStart);
buttonBackward.addEventListener("mouseup", onPressEnd);
//Android端
buttonBackward.addEventListener("touchstart", onPressStart);
buttonBackward.addEventListener("touchend", onPressEnd);
// 监听按钮点击事件
document.getElementById("btnStop").addEventListener("click", function () {
    flag_pause = 1;
    //自动暂停
    auto_detect = 0;
    const box = document.getElementById("btnStart");
    box.style.backgroundColor = "black";
    const box1 = document.getElementById("btnStop");
    box1.style.backgroundColor = "red";
    const box2 = document.getElementById("btnStart_hum");
    box2.style.backgroundColor = "black";
    popup = document.getElementById("direction-big");
    popup.style.display = "none";
    // 发送指令给消费者
    websocket.send(JSON.stringify({
        "command": "exit"
    }));
});
//小车连接
document.getElementById("car_start").addEventListener("click", function () {

    // 创建一个 div 元素作为容器
    var container = document.createElement("div");

    // 创建一个选择框
    var select = document.createElement("select");

    var textNode = document.createTextNode("请选择连接");
    select.appendChild(textNode);

    // 添加选项
    var option1 = document.createElement("option");
    option1.textContent = "创维机器人1011";
    select.appendChild(option1);

    // 创建一个确认按钮
    var button = document.createElement("button");
    button.textContent = "确认";

    // 将选择框和按钮添加到容器中
    container.appendChild(select);
    container.appendChild(button);

    // 设置容器的样式
    container.style.backgroundColor = "#1919a4"
    container.style.position = "absolute";
    container.style.left = '30%';
    container.style.top = "25%";
    container.style.border = "1px solid #ccc";
    container.style.padding = "10px";
    document.body.appendChild(container);
    button.addEventListener("click", function () {
        const car = document.getElementById("car_start");


        car.textContent = '正在连接'
        var interval = setInterval(function () {
            var text = car.textContent;
            if (text.length < 7) {
                text += ".";
            } else {
                text = "正在连接";
            }
            car.textContent = text;
        }, 500);
        // 等待三秒
        setTimeout(function () {
            clearInterval(interval);
            car.style.color = 'blue';
            car.style.fontWeight = 'bold';
            car.style.backgroundColor = "#fafa02";
            car.textContent = '已连接';
            car.textContent = '连接成功';
            container.style.display = "none";
        }, 3000);


    });

});
document.addEventListener('contextmenu', function (event) {
    event.preventDefault(); // 阻止浏览器默认右键菜单的显示
});







