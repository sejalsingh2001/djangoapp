from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.views import IsStaffOrReadOnly
from django.http import HttpResponse
from .models import Box
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import User

# Create your views here.

class box(APIView):
    permission_classes = [IsStaffOrReadOnly]
    # add box api
    def post(self,request):
        # print(request.POST)
        length = request.data.get('length')
        breadth = request.data.get('breadth')
        height = request.data.get('height')
        user = request.user

        print(length,breadth,height)
        print(user.username)
        box = Box(
            length = length,
            breadth = breadth,
            height = height,
            area = 2*(length*breadth+breadth*height+height*length),
            volume = length*breadth*height,
            user = user
        )
        box.save()

        return JsonResponse({'message': "Data saved with id"+str(box.id)})
    
    def patch(self,request):
        box_id = request.data.get('id')
        length = request.data.get('length')
        breadth = request.data.get('breadth')
        height = request.data.get('height')

        
        box = get_object_or_404(Box,id = box_id)

        box.length = length
        box.breadth = breadth
        box.height = height
        box.area  = 2*(length*breadth+breadth*height+height*length)
        box.volume = length*breadth*height
        box.save()

        return HttpResponse("Data updated of box id "+str(box.id))
    

    def get(self,request):
        
        box_list = []
        user = request.user
        boxes = Box.objects.filter(user = user)

        for box in boxes:
            box_list.append({
                "boxid" : box.id,
                "length" : box.length,
                "breadth" : box.breadth,
                "height" : box.height,
                "area" : box.area,
                "volume" : box.volume
                
            })
        return JsonResponse(box_list,safe=False)

    def delete(self,request):
        print("called")
        box_id = request.data.get('box_id')
        user = request.user

        box = get_object_or_404(Box,id = box_id)
        print("both users are " , box.user , user)
        if box.user != user:
            return JsonResponse({'message':"you are not authorised to delete the box"},status = 403)
        

        Box.objects.get(id = box_id).delete()
        return HttpResponse("deleted box with id "+str(box_id))


# third api 
# add permission for user authentication 
class allboxes(APIView):
    #  permission_classes = [IsAuthenticated]

    def get(self,request):
        box_list = []

        boxes = Box.objects.all()

        for box in boxes:
            box_list.append({
                "boxid" : box.id,
                "length" : box.length,
                "breadth" : box.breadth,
                "height" : box.height,
                "area" : box.area,
                "volume" : box.volume
                
            })
        return JsonResponse(box_list,safe=False)
