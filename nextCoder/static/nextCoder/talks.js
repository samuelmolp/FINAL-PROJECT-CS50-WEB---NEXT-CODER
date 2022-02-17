document.addEventListener("DOMContentLoaded", function() {
    //By default, get all of the data
    get_all_data();
    let title = document.querySelector(".talks_title");
    let filters = document.querySelector(".filters_div");
    title.innerHTML = "ALL TALKS";

    let form = document.querySelector("form");
    form.addEventListener("keyup", function(e){
        //When we enter text into the search bar, show the autocomplete
        if (e.key != 'Enter' || e.keyCode != 13) {
            if($("#search_title").val()!=""){
                filters.style.display = "none";
            } else {
                filters.style.display = "block";
            }
            document.querySelector(".suggestions").style.display = "flex";
            show_autocomplete();
        } else {
            filters.style.display = "block";
            document.querySelectorAll(".search_filters").forEach(function(element){
                $(element).find('option:eq(0)').prop('selected', true);
            });
        }
    });
    form.addEventListener("submit", function(){
        //If form is submitted, display the talks with the query
        display_results();
    });

    document.querySelectorAll(".search_filters").forEach(function(filter){
        filter.addEventListener("change", function(){
            //When we apply any of the filters:

            //Get all of the values of all of the filters
            let difficulty = $("#search_difficulty").children("option:selected").val();
            let language = $("#search_language").children("option:selected").val();
            let tool = $("#search_tool").children("option:selected").val();
            let area = $("#search_area").children("option:selected").val();
            let date = $("#search_date").children("option:selected").val();
            let max_people = $("#search_maxPeople").children("option:selected").val();
            let query = $("#search_title").val();


            if (difficulty!="" || language!="" || tool!="" || area!="" || date!="" || max_people!=""){
                //Call filter_tags for filtering the talks with the selected filters
                $(".talks_content").empty();
                filter_tags(difficulty, language, tool, area, query, date, max_people);

                //Add the title
                let title_text = `${difficulty} ${language} ${area} ${tool} ${date} ${max_people} TALKS`;
    
                if (query){
                    title_text = `"${query}"`+title_text;
                } 
                let text = title_text.replace("undefined", "");
                title.innerHTML = text;
            } else {
                //If no query, get talks by query or all talks
                $(".talks_content").empty();
                if (query){
                    title.innerHTML = `"${query}" TALKS`;
                    get_data_by_title(query);
                } else {
                    get_all_data();
                    title.innerHTML = "ALL TALKS";   
                }
            }
        });
    });
});


function display_results(){
    //Function to display the posts with the matching query or all of the posts if no query
    document.querySelector(".suggestions").style.display = "none";

    let title = $("#search_title").val();
    if (title==""){
        $(".talks_content").empty();
        document.querySelector(".talks_title").innerHTML = `ALL TALKS`;
        get_all_data();
    } else {
        document.querySelector(".talks_title").innerHTML = `"${title}" TALKS`;
        $(".talks_content").empty();
        get_data_by_title(title);
    }
}


function get_all_data(){
    //Function to get all data
    fetch(`/filter_talks/1`, {
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

function show_autocomplete(){
    //Function to make the autocomplete
    let text = $("#search_title").val();
    let html = "";
    let suggestions = document.querySelector(".suggestions_list");
    if(text!=""){
        //Make API call to get all of the talks that match the query
        fetch(`/filter_talks/1`, {
            method: 'POST',
            body: JSON.stringify({
                type:"query",
                query:text
            })
        })
        .then(response => response.json())
        .then(result => {
            //Show them in the suggestions div
            counter =0;
            for (element of result){
                if (counter<3){
                    html+=  `<p class="autocomplete_p" onclick='fun("${element["title"]}")'>${element["title"]}</p>`;
                    counter++;
                }
                else {
                    break;
                }
            }
            html+= `<p class="all_results" onclick="see_all()">See all results</p>`;
            suggestions.innerHTML = html;
        }); 
    } else {
        suggestions.innerHTML = "";
    }
    if ($(".suggestions_list > p").length <=1){
        document.querySelector(".suggestions").style.display = "none";
    }
}

function get_data_by_title(title){
    //Function to get the talks with the specified query
    fetch(`/filter_talks/1`, {
        method: 'POST',
        body: JSON.stringify({
            type:"query",
            query:title
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result["ERROR"] || result.length==0){
            $(".talks_content").empty();
            get_all_data();
            $( ".talks_content" ).prepend( "<p class='no_talks'>No matching talks, here are some other talks you may like:</p>" );
        } else {
            $(".talks_content").empty();
            show_talks(result);
        }
    });
}

function filter_tags(difficulty, language, tool, area, query,date ,max_people){
    //Function to filter the tags based on all specified arguments
    fetch(`/filter_talks/1`, {
        method: 'POST',
        body: JSON.stringify({
            type:"filter",
            difficulty:difficulty,
            language:language,
            tool:tool,
            area:area,
            query:query,
            date:date,
            max_people:max_people
        })
    })
    .then(response => response.json())
    .then(result => {
        $(".talks_content").empty();
        if (result.length===0){
            get_all_data();
            $( ".talks_content" ).prepend( "<p class='no_talks'>No matching talks, here are some other talks you may like:</p>" );
        } else {
            show_talks(result);
        }
    });
}
          

function see_all(){
    //Function called when see all button is cliked, call display_results
    document.querySelector(".filters_div").style.display = "block";
    display_results();
}


function fun(url){
    window.location.href = `/talk/${url}`;
}
