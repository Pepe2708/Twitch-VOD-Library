var data;

const getVideoInfo = async (sortBy, isAscending) => {
    const response = await fetch(`http://${ip}:8000/get-info/${sortBy}/${isAscending}`)
    const jsonResponse = await response.json() //extract JSON from the http response
    return await jsonResponse
  }

const getVideoAmount = async () => {
    const response = await fetch(`http://${ip}:8000/get-amount`)
    const jsonResponse = await response.json() //extract JSON from the http response
    return await jsonResponse
  }

async function cloneDraggables() {
    const videoAmount = await getVideoAmount()
    for (i = 1; i < videoAmount; i++) {
        clone = document.querySelector('#video-0').cloneNode(true)
        clone.setAttribute('id', 'video-' + i)
        document.querySelector('.container').appendChild(clone)
    }
}

async function editDraggables() {
    const attributes = ['id', 'length', 'date', 'streamer', 'category', 'title']
    data = await getVideoInfo(activeSort, sortState)
    const videoAmount = await getVideoAmount()
    for (videoId = 0; videoId < videoAmount; videoId++) {
        document.querySelector('#video-' + videoId).setAttribute('class', data[videoId][0] + ' draggable')

        for (attribute = 1; attribute < 6; attribute++) {
            document.querySelector('#video-' + videoId).querySelector('.' + attributes[attribute]).innerHTML = data[videoId][attribute]
        }

        if (data[videoId][7] == true) {updateIcon('.done', 'check_circle')}
        else if (data[videoId][7] == false) {updateIcon('.done', 'unpublished')}

        if (data[videoId][8] == true) {updateIcon('.favorite', 'star')}
        else if (data[videoId][8] == false) {updateIcon('.favorite', 'star_border')}

        function updateIcon(buttonClass, icon) {
            document.querySelector('#video-' + videoId).querySelector(buttonClass).childNodes[1].innerHTML = icon
        }
    }
}

async function addVideo() {
    const inputUrl = prompt("Enter link:")
    if (inputUrl != null) {
        document.querySelector('h3').innerHTML = "Loading..."
        const videoAmount = await getVideoAmount()
        const response = await fetch(`http://${ip}:8000/new-video`, {
            method: 'POST',
            headers: {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: inputUrl
            })
        }).catch( () => {
            document.querySelector('h3').innerHTML = "(Invalid link)"
        })
        const jsonResponse = await response.json() //extract JSON from the http response
        console.log(jsonResponse)
        clone = document.querySelector('#video-0').cloneNode(true)
        clone.setAttribute('id', 'video-' + (await getVideoAmount() - 1))
        document.querySelector('.container').appendChild(clone)
        editDraggables()
        moveVideo(videoAmount, 'top')
        document.querySelector('h3').innerHTML = ""
    }
}

async function deleteVideo(videoId) {
    const videoAmount = await getVideoAmount()
    if (videoAmount != 1) {
        const response = await fetch(`http://${ip}:8000/delete-video/${videoId}`, {
            method: 'DELETE',
            headers: {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
            }
        })
        console.log(response)
        for (i = 1; i < videoAmount; i++) {
            element = document.querySelector('#video-' + i)
            element.remove();
        }
        cloneDraggables()
        editDraggables()
    }
    else {
        document.querySelector('h3').innerHTML = "(Number of entries must be greater than zero)"
    }
}

async function openLink(videoId) {
    window.open(data[videoId][6])
}

async function toggleDone(videoId) {
    const response = await fetch(`http://${ip}:8000/update-done/${videoId}`, {
        method: 'PUT',
        headers: {'Access-Control-Allow-Origin': '*'}
    })
    const jsonResponse = await response.json() //extract JSON from the http response
    console.log(jsonResponse)
    editDraggables()
}

async function toggleFavorite(videoId) {
    const response = await fetch(`http://${ip}:8000/update-favorite/${videoId}`, {
        method: 'PUT',
        headers: {'Access-Control-Allow-Origin': '*'}
    })
    const jsonResponse = await response.json() //extract JSON from the http response
    console.log(jsonResponse)
    editDraggables()
}

async function moveVideo(videoId, direction) {
    console.log(videoId, direction)
    const response = await fetch(`http://${ip}:8000/change-order/${videoId}/${direction}`, {
        method: 'PUT',
        headers: {'Access-Control-Allow-Origin': '*'}
    })
    const jsonResponse = await response.json() //extract JSON from the http response
    console.log(jsonResponse)
    editDraggables()
}

async function updateDuration(videoId) {
    var duration = prompt('Enter duration (optional):');
    
    console.log(duration)
    if (duration == "") { duration = "00:00"; }
    const response = await fetch(`http://${ip}:8000/update-length/${videoId}`, {
        method: 'PUT',
        headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            length: duration
        })
    })
    const jsonResponse = await response.json() //extract JSON from the http response
    console.log(jsonResponse)
    editDraggables()
}

var activeSort = 0
var prevActiceSort = 0
var sortState = 0;
const sortByOptions = ['done', 'favorite', 'streamer', 'date', 'length']

function toggleSortBy(sortBy) {
    activeSort = sortBy
    
    if (prevActiceSort != activeSort) {
        sortState = 0;
    }

    if (sortState < 2) {
        sortState++;
    }
    else {
        sortState = 0;
        activeSort = 0;
    }

    prevActiceSort = activeSort

    for (i = 0; i < 5; i++) {
        var button = document.querySelector('#sort-' + sortByOptions[i]).children[0]
        button.classList.add('md-inactive')

        var arrow = document.querySelector('#sort-' + sortByOptions[i]).children[1]
        arrow.innerHTML = 'keyboard_arrow_up';
    }

    if (activeSort != 0) {
        switch (sortState) {
            case 0:
                var button = document.querySelector('#sort-' + activeSort).children[0]
                button.classList.add('md-inactive')
    
                var arrow = document.querySelector('#sort-' + activeSort).children[1]
                arrow.innerHTML = 'keyboard_arrow_up';
                break;
            case 1:
                var button = document.querySelector('#sort-' + activeSort).children[0]
                button.classList.remove('md-inactive')
                break;
            case 2:
                var button = document.querySelector('#sort-' + activeSort).children[0]
                button.classList.remove('md-inactive')
    
                var arrow = document.querySelector('#sort-' + activeSort).children[1]
                arrow.innerHTML = 'keyboard_arrow_down';
                break;
        }
    }
    editDraggables()
}
var ip = '192.168.1.237'