function init(){
    //Setup H2 groups
    titleElements = document.getElementsByClassName("titleRow");
    for (i=0;i<titleElements.length;i++) {
        titleElements[i].addEventListener("click", showHideGroup(titleElements[i]));
    }

    //Setup 'show more' list sections
    showElements = document.getElementsByClassName("showMore");
    for (i=0;i<showElements.length;i++) {
        showElements[i].addEventListener("click", ShowMore(showElements[i],"List"));
    }

        //Setup 'show more' table sections
    showTableElements = document.getElementsByClassName("showMoreTable");
    for (i=0;i<showTableElements.length;i++) {
        showTableElements[i].addEventListener("click", ShowMore(showTableElements[i],"Table"));
    }
}

function ShowMore(ele, ListOrTable){
    return function(){
        var siblings = ele.parentNode.parentNode.childNodes;
        if (ListOrTable == "List")
            siblings = ele.parentNode.childNodes;
        for (i=0;i<siblings.length;i++){
            sib = siblings[i];
            if (sib.classList && sib.classList.contains('hidden')){
                sib.classList.remove('hidden');
                sib.classList.add('canhide');
            }else if (sib.classList && sib.classList.contains('canhide')){
                sib.classList.remove('canhide');
                sib.classList.add('hidden');
            }
        }
        if (ele.innerHTML=="Show More"){
            ele.innerHTML="Hide";
        }else{
            ele.innerHTML="Show More";
        }

    }
}

function showHideGroup(ele){
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