import json
from users.models import MetaProfile, Profile
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from core.utils import accepted_response, check_torre_user,failed_response, search_common_interests

class LogIn(APIView):

    def post(self,request,*args,**kwargs):
        """
            Implements token auth creation 
        """
        pass

class LogInAsGuesst(APIView):

    def post(self,request,*args,**kwargs):
        """
            Creates a temporary user
        """
        all_ = User.objects.all().count()
        try:
            username = "guest-{}".format(all_+1)
            user = User.objects.create(username=username)
            profile = Profile.objects.create(user=user)
            return accepted_response({"id":profile.id})
        except:
            return failed_response("Problem creating your session")


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        """
            Destructs the auth token
        """
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return failed_response("User does not exist")
        try:
            token = Token.objects.get(user = user)
            token.delete()
        except:
            return failed_response("Something went wrong")

        return accepted_response("Succesfull logout")


class CreateUser(APIView):

    def post(self,request,*args,**kwargs):
        """
            Handles every new users, checking with 
            the torre API if user is available
        """
        username = request.POST.get('username')
        exist, info = check_torre_user(username)
        user = User.objects.get()




class SetMatch(APIView):

    def post(self,request,*args,**kwargs):
        try:
            """
                Creates a metauser and returns 
                the id
            """
            user_ = request.GET["id"]
            name = request.POST.get("name")
            username = request.POST.get("username")
            image_url = request.POST.get("image")

            try:
                user = MetaProfile.objects.get(username=username)
            except:
                user = MetaProfile.objects.create(username=username,
                                                  full_name=name,
                                                  image_url=image_url)
            
            profile = Profile.objects.get(id=user_)
            profile.matches.add(user)

            return accepted_response(json.dumps({"id":user.id}))
        except:
            return failed_response("Problem adding match")


class GetCoincidences(APIView):
    
    def post(self,request,*args,**kwargs):
        try:            
            id_ = request.GET["id"]
            size = request.GET["size"]
            
            profile = Profile.objects.get(id=id_)
            search_pref = request.POST.get("preferences")
            if not bool(size):
                # If any size is give, use 3 by default
                size = 1
    
            data = search_common_interests(json.loads(search_pref),size,'es')
            
            # Avoid showing users already matched !
            # only filter if user has matches
            if profile.matches.all().count() > 0:
                for e in data:
                        for user in profile.matches.all():
                            if e == user:
                                data.remove(user)
            
            return accepted_response(json.dumps({"results":data}))
            
        except:
            return failed_response("Any matches found")