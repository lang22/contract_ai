/***
 * 检查输入函数
 * @param domID
 * @param msgID
 * @param typeStr
 */
function check_input(domID, msgID, typeStr) {

    let idField = document.getElementById(domID);
    let url = "/gen/check_input_data?type=" + typeStr + '&data=' + idField.value.toString();
    let request;
    if (window.XMLHttpRequest) {
        request = new XMLHttpRequest();
    } else if (window.ActiveXObject) {
        request = new ActiveXObject("Microsoft.XMLHTTP");
    }

    request.open("GET", url, true);

    request.onreadystatechange = function () {
        if (request.readyState == 4) {
            if (request.status == 200) {
                let responseTest = request.responseText
                responseTest = JSON.parse(responseTest)
                let mdiv = document.getElementById(msgID);
                if (responseTest.code == "1") {
                    mdiv.innerHTML = "<font color='green'>" + responseTest.msg + "</font>";
                } else if (responseTest.code == "1") {
                    mdiv.innerHTML = "<font color='orange'>" + responseTest.msg + "</font>";
                } else {
                    mdiv.innerHTML = "<font color='red'>" + responseTest.msg + "</font>";
                }

            }
        }
    };
    request.send(null);
}