from django.shortcuts import render, redirect
from . models import Type, Setting, Cycle, Run
from subprocess import Popen, PIPE
process = 'process'
running = False
def takePictures(context: dict):
    global process
    global running
    running = True

    print(context)

    #process = Popen(["../a.out",str(pLen),str(interval),str(context["count"]),str(report)])
    #process = Popen(["../a.out",str(pLen),str(interval),str(context["count"]),str(bulb)])
    #print(process)

def cancelPictures():
    pass

def index(request):
    context = { 
        "pLen": "",
        "delay": "",
        "shutterType": "",
        "count": "",
        "bulb": False,
    }

    global running
    if running == True:
        return redirect('/running')

    if request.method == 'POST':
        context["shutterType"] = request.POST.get("shutterType")
        context["pLen"] = request.POST.get("pLen")
        context["delay"] = request.POST.get("delay")
        context["count"] = request.POST.get("count")
        bulb = request.POST.get("bulb")
        print(context)
        print(bulb)

        if(bulb == "true"): bulb = 1
        else: bulb = 2
        context["bulb"] = bulb

        if 'submit' in request.POST:
            takePictures(context)
            return redirect(f'/running')

        if 'clear' in request.POST:
            pass
        
        if 'click' in request.POST:
            return redirect(f'/clicking')



        print(request.POST)
        print(context)
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
        "pLen": "",
        "delay": "",
        "shutterType": "",
        "count": "",
        "bulb": "",
    }
    global process
    global running
    # Get info from curl/api
    

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
