from django.shortcuts import render, redirect
from . models import Type, Setting, Cycle, Run
from subprocess import Popen, PIPE
import requests, json
process = 'process'
running = False
runningContext = {}

def takePictures():
    global process
    global running
    global runningContext
    running = True

    print("takePictures - runningContext " + str(runningContext))
    content = requests.get('http://127.0.0.1:8000/').content
    content = json.loads(content.decode('utf-8'))
    

    #process = Popen(["../a.out",str(pLen),str(interval),str(context["count"]),str(report)])
    #process = Popen(["../a.out",str(pLen),str(interval),str(context["count"]),str(bulb)])
    #print(process)

def cancelPictures():
    pass

def index(request):
    global runningContext
    context = { 
        "pLen": "",
        "delay": "",
        "shutterType": "",
        "count": "",
        "bulb": None,
    }

    global running
    if running == True:
        return redirect('/running')

    if request.method == 'POST':
        context["shutterType"] = request.POST.get("shutterType")
        context["pLen"] = request.POST.get("pLen")
        context["delay"] = request.POST.get("delay")
        context["count"] = request.POST.get("count")
        context["bulb"] = request.POST.get("bulbMode")
        print(context)

        if(context["bulb"] == "b"): context["bulb"] = 1
        else: context["bulb"] = 0

        print("index - context " + str(runningContext))

        runningContext = context

        if 'submit' in request.POST:
            takePictures()
            return redirect(f'/running')

        if 'clear' in request.POST:
            pass
        
        if 'click' in request.POST:
            return redirect(f'/clicking')



        print(request.POST)
        
    return render(request, 'dashboard/index.html', context)

def clicking(request):
    context = {}

    global running
    if running == True:
        return redirect('/running')

    if request.method == 'POST':
        if 'clicking' in request.POST:
            #Run clicking command
            pass

        if 'home' in request.POST:
            return redirect(f'/')

        #print(request.POST)
        #print(context)
    return render(request, 'dashboard/clicking.html', context)


def running(request):
    context = { 
        "top": 0,
        "bottom": 0,
    }
    global process
    global running
    global runningContext
    # Get info from curl/api
    print("running - runningContext " + str(runningContext))

    if request.method == 'POST':
        if 'index' in request.POST:
            if(context["top"] == context["bottom"]):
                running = False
                return redirect("index")

        if 'cancel' in request.POST:
            try:
                process.kill()
            except:
                pass
            running = False
            return redirect("index")

        if 'again' in request.POST:
            
            takePictures(context)
            return redirect(f'/running')
        print(context)

    return render(request, 'dashboard/running.html', context)
