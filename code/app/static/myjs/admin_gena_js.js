/***
 *  ajax Get请求通用函数，请求一个
 *
 * @param baseURL
 * @param paraDict
 * @param onReadyStateChangeFunc
 */
/**
 * 合同业务内容
 * @type {null}
 */
let contentDict = null;

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
                console.log(request.responseText)
                onReadyStateChangeFunc(JSON.parse(responseText));
            }
        }
    };
    request.send(null);
}


function change(contracts) {
    let xz_ejfl = document.getElementById("xz_ejfl");
    xz_ejfl.length = 1;
    for (let i = 0; i < contracts.conLen; i++) {
        xz_ejfl.options.add(new Option(contracts.conNames[i], contracts.conPid[i]))
    }
    let tableContent = document.getElementById("tableContentId");
    contentDict = contracts.conContent
}

/***
 * 当改变Select的时候，请求后台获取数据
 * @param value 选择合同
 */
function onContractSelectChange(value) {
    console.log('onContractSelectChange(' + value + ')')
    ajaxGet("/gen/choose_contract", {'value': value}, change)

}


/**
 * 改变
 * @param value
 */
function selectChange(value) {
    let tableContent = document.getElementById("tableContentId");
    tableContent.innerText = contentDict[value];
}

/**
 * 提交验证
 */
function sb1() {
    let xz_ejfl = document.getElementById("xz_ejfl");
    if (xz_ejfl.selectedIndex == '00000') {
        alert("请选择一个合同业务！");
    }
    else {
        let form1 = document.getElementById('docx_type')
        form1.submit()
    }
}


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