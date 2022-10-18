/**
 * 导出HttpClient文件
 */


/***
 *  ajax Get请求通用函数，请求一个
 *
 * @param baseURL
 * @param paraDict
 * @param onReadyStateChangeFunc
 */

function ajaxGet(baseURL, paraDict, onReadyStateChangeFunc) {

    let url = createURL(baseURL, paraDict)
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
                let responseText = request.responseText;
                onReadyStateChangeFunc(JSON.parse(responseText));
            }
        }
    };
    request.send(null);
}

export default ajaxGet;

/***
 *  根据参数拼接字典
 * @param paraDict
 * @returns {string}
 */
function createURL(baseURL, paraDict) {
    let output = baseURL + "?";
    for (let key in paraDict) {
        output += key + '=' + paraDict[key] + '&';
    }
    return output
}

