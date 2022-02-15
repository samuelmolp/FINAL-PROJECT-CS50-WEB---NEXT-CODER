//Javascript for the new_talk pages

document.addEventListener("DOMContentLoaded", function(){
    if (window.location.pathname==="/new_talk/2"){
        //Hide the new_talk/1 form and display the page for adding tags
        document.querySelector("#first").style.display = "none";
        document.querySelector("#second").style.display = "block";
        document.querySelector("#new_talk_title").innerHTML = "We're almost there...";
        getTags();
    } 
});

function getTags(){
    //Fetch to get a json of all of the tags in the database
    fetch('/tags')
    .then(response => response.json())
    .then(words => {
        //Function to display the tags
        add(words);
    });
}


function add(words){
    //Function to display the given posts
    let tag1 = document.querySelector("#tags1_list");
    let tag2 = document.querySelector("#tags2_list");
    
    for (let tag of words["tags1"]){
        let item = document.createElement("div");
        item.innerHTML= tag;
        item.classList.add("rectangles");
        item.classList.add("notClicked");
        item.addEventListener("click", function(){
            //When clicked, change color
            if (item.classList.contains("clicked")){
                item.classList.remove("clicked");
                item.classList.add("notClicked");
            } else {
                item.classList.remove("notClicked");
                item.classList.add("clicked");
            }
            //And add/remove the tag
            add_removeTag(tag);
        });
        tag1.append(item);
    }

    for (let tag of words["tags2"]){
        let item = document.createElement("div");
        item.innerHTML= tag;
        item.classList.add("rectangles");
        item.classList.add("notClicked");
        item.addEventListener("click", function(){
            if (item.classList.contains("clicked")){
                item.classList.remove("clicked");
                item.classList.add("notClicked");
            } else {
                item.classList.remove("notClicked");
                item.classList.add("clicked");
            }
            add_removeTag(tag, item);
        });
        tag2.append(item);
    }

    //Add the buttons for creating a new tag
    for (let i=0;i<2;i++){
        let newTag = document.createElement("div");
        newTag.innerHTML = "New tag";
        newTag.classList.add("rectangles");
        newTag.classList.add("new_tag");
        newTag.addEventListener("click", function(){
            //When clicked, call the function to create a new tag
            create_tag(i+1);
        })
        if (i==0){
            tag1.append(newTag);
        } else {
            tag2.append(newTag);
        }
    }

    document.querySelector("#finish").addEventListener("click", function(){
        //When clicking the finish button, check that the user hasn't selected 
        //more than three tags of each kind
        fetch('/new_talk/2', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(result => {
            if (result["len1"]>3 || result["len2"]>3){
                //If the user has provided too many tags, alert him and fetch to delete the selected tags
                alert("You cannot provide more than three tags of each category");
                fetch('/new_talk/2', {
                    method: 'PUT',
                    body: JSON.stringify({
                        tag: "delete"
                    })
                })
                .then(response => response.json())
                .then(result => {
                    window.location.reload();
                })
            } else {
                //Otherwise, return to talks
                window.location.href = "/talks";
                alert("The talk was added succesfully");
            }
        });
    });
}

function add_removeTag(tag){
    //Fetch for add/remove the a given tag
    fetch('/new_talk/2', {
        method: 'PUT',
        body: JSON.stringify({
            tag: tag
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result!=200){
            alert("Forbidden");
            window.location.href="/";
        }
    });
}

function create_tag(type){
    //When clicking the create new tag button, prompt for the text, and call the function
    let text = prompt("Enter name of new tag");
    newTag(text, type);
}

function newTag(text, type){
    //Fetch for adding the new tag to the database
    fetch('/tags', {
        method: 'POST',
        body: JSON.stringify({
            name: text,
            type: type
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result==200){
            fetch('/new_talk/2', {
                method: 'PUT',
                body: JSON.stringify({
                    tag: "delete"
                })
            })
            .then(response => response.json())
            .then(result => {
                window.location.reload();
            })       
        } else {
            alert("It must be a new tag (there is already one with that name)");
        }
    });
}
