(function () {
    let url = window.location.pathname
    if (url == '/'){
        $('#recent').addClass('linking')
    }
    if (url== '/my/gifts'){
        $('#gifts').addClass('linking')
    }
    if (url == '/my/wish'){
        $('#wishes').addClass('linking')
    }
    if (url == '/wallpaper/top'){
        $('#pending').addClass('linking')
    }
})()