#imports
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import query
from django.forms.forms import Form
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django import forms
import datetime
import json
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage


from .models import Tags, User, Talks




class newTalkForm(forms.Form):
    """
    Form for creating a talk
    """

    #Get the different choices
    obj = Talks()
    difficulty_choices = obj.get_difficulty()
    duration_choices = obj.get_duration()
    language_choices = obj.get_language()

    title = forms.CharField(label="", widget=forms.TextInput(attrs={'autocomplete':'off', "autofocus":True, "placeholder":"TITLE", "id":"new_talk_title_form"}), max_length=50)
    text = forms.CharField(label="Description", widget=forms.Textarea(attrs={'autocomplete':'off', "placeholder":"Description", "id":"new_talk_descr"}))
    max_people = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder":"Max attendants"}))
    talk_date = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    start_hour = forms.TimeField(widget=forms.TimeInput(attrs={"type":"time"}))

    difficulty = forms.CharField(widget=forms.Select(choices=difficulty_choices))
    language = forms.CharField(widget=forms.Select(choices=language_choices))
    duration = forms.CharField(widget=forms.Select(choices=duration_choices))

    about_author = forms.CharField(label="About the author", widget=forms.Textarea(attrs={'autocomplete':'off', "placeholder":"Tell us something about who gives the talk", "id":"new_talk_aboutAuthor"}))
    prerrequesites = forms.CharField(label="Prerrequestites", widget=forms.Textarea(attrs={'autocomplete':'off', "placeholder":"Tell us if there are any prerrequestites (things people should already know before the talk)", "id":"new_talk_prerrequestites"}))
    how_how_to_attend_meeting = forms.CharField(label="How to attend the meeting", widget=forms.Textarea(attrs={'autocomplete':'off', "placeholder":"Explain how to attend the meeting for the people who are enrolled (it will only appear to those who are enrolled). Add any links to zoom, meet or whichever platform you're planning to use. ", "id":"new_talk_prerrequestites"}))

    

def index(request):
    #We return the main page
    return render(request, "nextCoder/index.html")

def talks(request):
    #We return the page to display the current talks
    if request.method=="GET":
        return render(request, "nextCoder/talks.html", {
            "form":searchTalkForm()
        })




#FUNCTION COPIED FROM SOURCE CODE FOR PROJECT 4. Function to login
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "nextCoder/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "nextCoder/login.html")


#FUNCTION COPIED FROM SOURCE CODE FOR PROJECT 4. Function to logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


#FUNCTION COPIED FROM SOURCE CODE FOR PROJECT 4. Function to register
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "nextCoder/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "nextCoder/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "nextCoder/register.html")


@csrf_exempt
def new_talk(request, type):
    """
    Function for saving new talks
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if type==1:
        """
        We're at /new_post/1, responsible for creating a new post 
        """ 
        if request.method=="POST":
            """
            If the method is post, the form has been sent so we collect the data 
            and store it in the model
            """
            
            form = newTalkForm(request.POST)

            if form.is_valid():
                #Collect the data
                title = form.cleaned_data["title"]
                text = form.cleaned_data["text"]
                max_people = form.cleaned_data["max_people"]
                talk_date = form.cleaned_data["talk_date"]
                start_hour = form.cleaned_data["start_hour"]
                duration = form.cleaned_data["duration"]
                language = form.cleaned_data["language"]
                difficulty = form.cleaned_data["difficulty"]
                about_author = form.cleaned_data["about_author"]
                prerrequesites = form.cleaned_data["prerrequesites"]
                how_how_to_attend_meeting = form.cleaned_data["how_how_to_attend_meeting"]
                

            else:
                #Return the form if there's an error
                return render(request, "nextCoder/new_talk.html", {
                    "form": form
                })


            #Get the image and store it
            try:
                img = request.FILES["img"]
                fs = FileSystemStorage()
                name = fs.save(img.name, img)
                url = fs.url(name)

            except KeyError:
                url = None

            user = request.user
            date = datetime.datetime.now()

            #Save the data to the model
            Talks(creator=user, date=date, description=text, title=title, image=url,
                max_people=max_people, talk_date=talk_date, start_hour=start_hour,
                duration=duration, language=language, difficulty=difficulty, prerrequesites=prerrequesites,
                about_author=about_author, how_to_attend_meeting=how_how_to_attend_meeting).save()

            #Redirect to new_talk/2
            return HttpResponseRedirect(reverse("new_talk",  kwargs={"type":2}))

        else:
            try:
                #Check that the user hasn't created any other talk today
                obj = Talks.objects.filter(creator=request.user).order_by("-date")[0]
                if obj.date == datetime.date.today():
                    return render(request, "nextCoder/new_talk.html", {
                        "error":"You can only create one talk each day"
                    })

            except:
                pass
            
            
            #Return new_talk.html with the django form ¡
            return render(request, "nextCoder/new_talk.html", {
                "form":newTalkForm()
            })

    else:
        if request.method=="PUT":
            """
            Add/remove tags
            """
            data = json.loads(request.body)

            try:
                obj = Talks.objects.filter(creator=request.user).order_by("-date")[0]
            except:
                return JsonResponse({"error":"forbidden"})

            existing_tags = obj.tags.all()

            if data["tag"]=="delete":
                #If in the fetch request it says delete, delete all tags of a talk
                for tag in existing_tags:
                    obj.tags.remove(tag)
                return HttpResponse(200)

            else:
                #Add a tag to a talk
                tag = Tags.objects.get(tag1=data["tag"])
                
                if tag in existing_tags:
                    obj.tags.remove(tag)
                else:
                    obj.tags.add(tag)

                return HttpResponse(200)

        elif request.method=="POST":
            """
            Return a the number of tags that a talk has (divided by type1 and type2)
            """
            obj = Talks.objects.filter(creator=request.user).order_by("-date")[0]
            existing_tags = obj.tags.all()

            tag1 = Tags.objects.filter(type=1).values_list("tag1", flat=True)
            tag2 = Tags.objects.filter(type=2).values_list("tag1", flat=True)

            tags = []
            for e in existing_tags:
                tags.append(e.tag1)


            num1 = 0
            num2 = 0
            for e in tags:
                if e in tag1:
                    num1+=1

                elif e in tag2:
                    num2+=1

            return JsonResponse({"len1":num1, "len2":num2})


        else:
            #Return new_takl.html
            return render(request, "nextCoder/new_talk.html")
            

@csrf_exempt
def tags(request):
    if request.method=="GET":
        """
        Return a json of all the tags in the database
        """
        tags = get_tags()

        return JsonResponse({"tags1":tags[0], "tags2":tags[1]})

    else:
        """
        Create a new tag and store it in the database
        """
        data = json.loads(request.body)
        tags = Tags.objects.values("tag1")
        tag_list = []
        for e in tags:
            tag_list.append(e["tag1"])
        
        name = data["name"]
        if name in tag_list or name.upper() in tag_list or name.lower() in tag_list or name.capitalize() in tag_list:
            return JsonResponse({"error":"must be a new one"})

        Tags(tag1=data["name"], type=data["type"]).save()
        return HttpResponse(200)



def get_tags():
    """
    Return a list with all of the tags
    """
    tags1 = Tags.objects.filter(type=1)
    tags2 = Tags.objects.filter(type=2)
    tag1 = []
    tag2 = []
    for tag in tags1:
        tag1.append(tag.tag1)

    for tag in tags2:
        tag2.append(tag.tag1)

    return [tag1, tag2]



@csrf_exempt
def filter_talks(request, page):
    """
    Function to return a list of talks based on the filters that the user selected
    """
    data = json.loads(request.body)

    if data["type"]=="all":
        #If type is all, return all talks
        final = Talks.objects.all()

    elif data["type"]=="query":
        """
        If type is query, call the get_by_title function to return posts in which
        the text that the user has typed in search bar appears in the title, description or tags
        """
        final = get_by_title(data["query"])
        if talks == "ERROR":
            return JsonResponse({"ERROR":"No matching talks"})

    elif data["type"]=="filter":
        """
        If type is filter, we filter based on different parametres
        """
        all_talks = list(Talks.objects.all())
        filtered_talks_dl = list(all_talks)

        #Filter by difficulty and language
        for talk in all_talks:
            if talk.difficulty != data["difficulty"] and data["difficulty"]!="":
                filtered_talks_dl.remove(talk)

            if talk.language != data["language"] and data["language"]!="":
                try:
                    filtered_talks_dl.remove(talk)
                except ValueError:
                    pass

        #Filter by tool and area
        filtered_talks_dlta = list(filtered_talks_dl)
        for e in filtered_talks_dl:
            tags = e.tags.all()
            if data["tool"]!="":
                tag = Tags.objects.get(tag1=data["tool"])
                if tag not in tags:
                    try:
                        filtered_talks_dlta.remove(e)
                    except ValueError:
                        pass
            if data["area"]!="":
                tag = Tags.objects.get(tag1=data["area"])
                if tag not in tags:
                    try:
                        filtered_talks_dlta.remove(e)
                    except ValueError:
                        pass  

        #Filter by date
        filtered_talks_dltad = list(filtered_talks_dlta)  
        for element in filtered_talks_dlta:
            if data["date"]=="Today":
                if str(element.date)!=datetime.datetime.now().strftime("%Y-%m-%d"):
                    filtered_talks_dltad.remove(element)

            elif data["date"]=="Tomorrow":
                tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                if str(element.date)!=tomorrow.strftime("%Y-%m-%d"):
                    filtered_talks_dltad.remove(element)

            elif data["date"]=="Next 7 days":
                next_week = datetime.datetime.now() + datetime.timedelta(days=7)
                if str(element.date)>next_week.strftime("%Y-%m-%d") or str(element.date)<=datetime.datetime.now().strftime("%Y-%m-%d"):
                    filtered_talks_dltad.remove(element)

            elif data["date"]=="Next 30 days":
                new_month = datetime.datetime.now() + datetime.timedelta(days=30)
                if str(element.date)>new_month.strftime("%Y-%m-%d") or str(element.date)<=datetime.datetime.now().strftime("%Y-%m-%d"):
                    filtered_talks_dltad.remove(element)
            
            elif data["date"]=="Later":
                new_month = datetime.datetime.now() + datetime.timedelta(days=30)
                if str(element.date)<new_month.strftime("%Y-%m-%d"):
                    filtered_talks_dltad.remove(element)


        #Filter by max_people
        final_filtered_talks = list(filtered_talks_dltad)
        for element in filtered_talks_dltad:
            if data["max_people"]=="0-10":
                if element.max_people<0 or element.max_people>10:
                    final_filtered_talks.remove(element)

            elif data["max_people"]=="10-50":
                if element.max_people<10 or element.max_people>50:
                    final_filtered_talks.remove(element)

            elif data["max_people"]=="50-100":
                if element.max_people<50 or element.max_people>100:
                    final_filtered_talks.remove(element)

            elif data["max_people"]=="100-500":
                if element.max_people<100 or element.max_people>500:
                    final_filtered_talks.remove(element)

            elif data["max_people"]=="+500":
                if element.max_people<500:
                    final_filtered_talks.remove(element)

        #filter by query
        query_talks = get_by_title(data["query"])
        if query_talks=="ERROR":
            return JsonResponse({"ERROR":"No matching talks"})

        final = list(final_filtered_talks)
        for e in final_filtered_talks:
            if e not in query_talks:
                final.remove(e)

    #Serialize results and paginate them
    results = []
    for e in final:
        if e.serialize() not in results:
            results.append(e.serialize())

    results.reverse()
        
    #Return the data (or an error)
    return JsonResponse(results, safe=False)
            


def get_by_title(query):
    """
    Return talks in which the words appear in title, description or tags
    """
    try:
        talks = list(Talks.objects.filter(title__contains=query))
    except Talks.DoesNotExist:
        return "ERROR"

    talks_descr = list(Talks.objects.filter(description__contains = query))
    talks.extend(talks_descr)

    try:
        tag = Tags.objects.filter(tag1__contains=query)
        for element in tag:
            talks.extend(list(Talks.objects.filter(tags__in = [element])))
        
    except Tags.DoesNotExist:
        pass

    return talks




class searchTalkForm(forms.Form):
    """
    Class for the search filters in /talks
    """
    #Get the different choices
    obj = Talks()
    difficulty_choices = obj.get_difficulty()
    language_choices = obj.get_language()

    tags = get_tags()
    
    area_choices = [(e,e) for e in tags[0]]
    tool_choices = [(e,e) for e in tags[1]]
    area_choices.insert(0,("", "Area"))
    tool_choices.insert(0,("", "Tool"))

    date_choices = [("", "Date"),("Today", "Today"), ("Tomorrow", "Tomorrow"), ("Next 7 days", "Next 7 days"), ("Next 30 days", "Next 30 days"), ("Later", "Later")]

    max_people_choices = [("", "Max people"), ("0-10", "0-10"), ("10-50", "10-50"), ("50-100", "50-100"), ("100-500", "100-500"), ("+500", "+500")]

    
    #Filters
    difficulty = forms.CharField(label="", widget=forms.Select(choices=difficulty_choices, attrs={"id":"search_difficulty", "class":"search_filters form_talks_fields"}), required=False)
    language = forms.CharField(label="", widget=forms.Select(choices=language_choices, attrs={"id":"search_language", "class":"search_filters form_talks_fields"}), required=False)
    area = forms.CharField(label="", widget=forms.Select(choices=area_choices, attrs={"id":"search_area", "class":"search_filters form_talks_fields"}), required=False)
    tool = forms.CharField(label="", widget=forms.Select(choices=tool_choices, attrs={"id":"search_tool", "class":"search_filters form_talks_fields"}), required=False)
    date = forms.CharField(label="", widget=forms.Select(choices=date_choices, attrs={"id":"search_date", "class":"search_filters form_talks_fields"}), required=False)
    max_people = forms.CharField(label="", widget=forms.Select(choices=max_people_choices, attrs={"id":"search_maxPeople", "class":"search_filters form_talks_fields"}), required=False)


def talk(request, title):
    """
    Get information about a talk by it's title
    """
    if request.method=="GET":
        try:
            talk = Talks.objects.get(title=title)
            data = [talk.serialize()]

        except Talks.DoesNotExist:
            data = "error"

        return render(request, "nextCoder/talk.html", {
            "data":data[0], 
            "isAttendant":request.user in talk.attendants.all()
        })

@csrf_exempt
def enroll(request, title):
    """
    Function to enroll in a course
    """
    if request.method=="POST":
        talk = Talks.objects.get(title=title)
        user = request.user

        if user in talk.attendants.all():
            talk.attendants.remove(user)
            return JsonResponse({"enrolled":False})
        else:
            talk.attendants.add(user)
            return JsonResponse({"enrolled":True})

def my_talks(request):
    """
    Load mytalks view
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "nextCoder/my_talks.html")

@csrf_exempt
def get_enrrolled_talks(request):
    """
    Get all of the talks in which the current user is enrolled
    """
    user = request.user
    talks= Talks.objects.all()

    enrolled_talks = []
    for talk in talks:
        if user in talk.attendants.all():
            enrolled_talks.append(talk.serialize())

    return JsonResponse(enrolled_talks, safe=False)