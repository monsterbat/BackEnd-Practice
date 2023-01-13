let main = document.getElementById("main")
let uploadButton = document.getElementById('imgChoose');
let inputContent = document.getElementById('inputContent');
let connectAlarm = document.getElementById('connectAlarm');
let imageAlarm = document.getElementById('imageAlarm');
let imageData = null
let submit = document.getElementById('submit');

// On load process
getImageSrc()
async function getImageSrc(){
    return fetch("api/image",{
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    }).then(function(response){
        return response.json();
    }).then(function(data){
        for(i=0;i<Object.keys(data).length;i++){
            createElement(main, "div", "sparate", "sparate")
            createElement(main, "img", "image","image", data[i]["imageUrl"])
            createElement(main, "div", "connect","connect", data[i]["connent"])
        }
        return data
    })
}
// Click uploadButton create image data
uploadButton.addEventListener('click', function() {
    // Open file selector when upload button is clicked
    document.getElementById('file-uploader').click();
});
let fileInput = document.getElementById('file-uploader');
fileInput.addEventListener('change', async function(e) {
    let blob = e.target.files[0]
    let imageType = e.target.files[0].type.slice(6)
    let reader = new FileReader()
    reader.readAsArrayBuffer(blob)
    reader.onload = async function(){
        let arrayBuffer = reader.result
        let imageRaw = new Uint8Array(arrayBuffer);
        imageRaw = Array.from(imageRaw)
        imageData = {
            "image_type":imageType,
            "image_raw":imageRaw,
        }     
    }
});


// Submit
submit.addEventListener('click', sentToDatabass)
async function sentToDatabass(){
    if(inputContent.value =="" && imageData == null){
        connectAlarm.style.display="block"
        return imageAlarm.style.display="block"
    }
    if (inputContent.value ==""){
        imageAlarm.style.display="none"
        return connectAlarm.style.display="block"
    }
    if (imageData == null){
        connectAlarm.style.display="none"
        return imageAlarm.style.display="block"
    }
    let connect = {
        "connent":inputContent.value
    }
    imageAlarm.style.display="none"
    connectAlarm.style.display="none"
    let sourceData = Object.assign({}, imageData, connect);
    newData = await fetchData(sourceData)
    createElement(main, "div", "sparate", "sparate")
    createElement(main, "img", "image", "image", newData.imageUrl)
    createElement(main, "div", "connect", "connect",newData.connent)
    
}

async function fetchData(data){
    return fetch("api/image",{
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    }).then(function(response){
        return response.json();
    }).then(function(data){
        return data
    })
}


// creat element Function
function createElement(appendBlock, elementStyle, addId = null, addClass = null, addText = null){
    element = document.createElement(elementStyle);
    if (addId != null){
        element.setAttribute("id",addId);
    }
    if (addClass != null){
        element.setAttribute("class",addClass);   
    }
    if (elementStyle == "img"){
        element.src = addText;
    }
    else{
        element.textContent = addText;
    }
    appendBlock.prepend(element);
    globalThis.addId = document.getElementById(addId)
}
