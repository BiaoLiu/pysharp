from django.shortcuts import render

# Create your views here.

def test(request):
    # return render(request,'wechat/test.html')
    # return render_to_response('wechat/test.html')
    return render(request,'wechat/test.html',{'TEST':'testtesttest'})
