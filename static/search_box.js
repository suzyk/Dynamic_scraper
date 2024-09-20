const searchInput = document.querySelector("#search"); 
const searchBox = document.querySelector(".search-box");
const searchIcon = document.querySelector(".search-icon");
const goIcon = document.querySelector(".go-icon");
const searchForm = document.querySelector(".search-form");

if (document.readyState !== 'loading') {
    console.log('document is already ready, just execute code here');
    myInitCode();
} else {
    document.addEventListener('DOMContentLoaded', function () {
        console.log('document was not ready, place code here');
        myInitCode();
    });
}

function myInitCode(){
    searchInput.addEventListener("focus", handleSearchFocus);
    searchInput.addEventListener("blur", handleSearchNotFocus);
    searchInput.addEventListener("keyup", handleSearchKeyup);
    goIcon.addEventListener("onclick", handleGoIconClick);
}

function handleSearchFocus(){
    searchBox.classList.add("border-searching");
    searchIcon.classList.add("si-rotate");
}

function handleSearchNotFocus(){
    searchBox.classList.remove("border-searching");
    searchIcon.classList.remove("si-rotate");
}

function handleSearchKeyup(){
    if (searchInput.value.length > 0){
        goIcon.classList.add("go-in");
    }else{
        goIcon.classList.remove("go-in");
    }
}

function handleGoIconClick(){
    console.log("inside go click")
    searchForm.submit();
}
