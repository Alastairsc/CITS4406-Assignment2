function init(){
    titleElements = document.getElementsByClassName("titleRow");
    for (i=0;i<titleElements.length;i++) {
        titleElements[i].addEventListener("click", showHide(titleElements[i]));
    }
}

function showHide(ele){
    return function(){
        var siblings = ele.parentNode.childNodes;
        passedMyself = false;
        for (i=0;i<siblings.length;i++){
            sib = siblings[i];
            if (sib==ele){
                passedMyself = true;
                continue;}
            if (passedMyself && sib.classList ){
                if (sib.tagName==="H2")
                break;
                if (sib.classList.contains('hidden'))
                    sib.classList.remove('hidden');
                else
                    sib.classList.add('hidden');
            }
        }
    } 
}