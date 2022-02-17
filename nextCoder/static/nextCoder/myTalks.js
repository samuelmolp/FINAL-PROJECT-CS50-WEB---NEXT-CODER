document.addEventListener("DOMContentLoaded", function(){
    load_talks();
});

function load_talks(){
    fetch(`/get_enrrolled_talks`, {
        method: 'POST',
        body: JSON.stringify({
            type:"all"
        })
    })
    .then(response => response.json())
    .then(result => {
        show_talks(result);
    });
}

function show_talks(result){
    //Function to show the talks passed as arguments in the DOM
    let content = document.querySelector(".talks_content");
    for (element of result){
        let div = document.createElement("div");
        div.classList.add("card");
        div.classList.add("talk");
        div.dataset.aos="fade-up";
        div.dataset.title = element.title;
        date = element.date.replace("-", "/");
        hour = element.start_hour.slice(0,-3);
        date = `${element.date[8]}${element.date[9]}/${element.date[5]}${element.date[6]}/${element.date[0]}${element.date[1]}${element.date[2]}${element.date[3]}`

        div.innerHTML = `
            <img src="${element.image}" alt="talk image">
            <h4>${element.title}</h4>
            <p class="talks_date">${element.date}: ${hour}</p>
            <p class="creator">${element.creator}</p>
            <p class="language">${element.language}</p>`;


        div.addEventListener("click", function(){
            window.location.href = `/talk/${div.dataset.title}`;
        });
        content.append(div);
    }

    let footer = document.createElement("div");
    footer.classList.add("footer");
    footer.innerHTML = `
            <address>
                Made by Samuel Molina Perales.
                Contact me at: <a href="mailto:smolinaperales@gmail.com">smolinaperales@gmail.com</a>
            </address>
            <p class="copy">Next coder. All rights deserved &#169; 2021</p>`
    content.append(footer);
}