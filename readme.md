# CS50 WEB PROGRAMMING FINAL PROJECT: NEXT CODER

The project video is: https://youtu.be/YtHHEC-bdqA

## Main idea
I created a collaborative web application to learn how to code. Everyone can create a talk (which are basically just classes) and everyone can enroll in those classes. The main components are:

* Home page
* Login/Logout/Register
* Talks page in which there are listed all of the different talks or classes and where you can filter talks by different criterias
* An individual page for each talk with all of it's information and a button to enroll
* A page in which you can access all of the talks in which you are enrolled
* A page to create new talks


## Distinctiveness and Complexity
The page is not similar to anything we have already created. It's not a social media app nor an e-commerce. It's not similar to other years projects either. 

In terms of complexity, I used Django with more than one model (explained below) and several javascript files to the frontend. 
Moreover, all of the web application is responsive to the different screen sizes (mainly mobile phones and computers).

## Files information

* In views.py there is all of the backend code. The main functions are:
    * Class newTalkForm with all the fields for creating a new talk
    * Class searchTalkForm for filtering talks
    * Login, logout and register functions copied from project 4
    * New_talk for saving a new talk and related information likes tags
    * Tags for retrieving existing tags and adding new ones
    * Filter tags: to return a list of talks based on the filters that the user selected
    * Get_by_title: return talks in which the words appear in title, description or tags
    * Talk to retrieve information about a specific talk
    * Enroll: to enroll a talk
    * Get_enrolled_talks: to retrieve the talks in which you are enrolled

* Models.py. The different models are:
    * A users model
    * A model for tags
    * A model talks with all of the different details about a talk (and a serializer)


* Talks.js: to filter talks, show the talks and autocomplete when you search for a talk
* New_talk.js: For the second part of creating a new talk which is adding tags. It loads and shows tags, saves new tags and adds the selected tags to the new talk
* MyTalks.js: to get the talks in which you are enrolled and show them in the DOM

* Templates for all of the different html pages explained above (8 in total including a layout file)
* A css file with all of the css used in the web application. Techniques like flexbox and grid are used
* Other less important files like urls, admin, settings, static images...

## How to run the application
* Install project dependencies by running pip install -r requirements.txt
* Make and apply migrations by running python manage.py makemigrations and python manage.py migrate.
