import json
from users.models import MetaProfile, Profile
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from core.utils import accepted_response, check_torre_user,failed_response, get_profile_by_id, search_common_interests

class LogIn(APIView):

    def post(self,request,*args,**kwargs):
        """
            Implements token auth creation 
        """
        pass

class LogInAsGuest(APIView):

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

            return accepted_response(json.dumps({"username":username,
                                                 "name":name,
                                                 "image":image_url}))
        except:
            return failed_response("Problem adding match")

class GetMatches(APIView):

    def get(self,request,*args,**kwargs):
        profile = get_profile_by_id(int(request.GET["id"])) 
        matches = []
        for m in profile.matches.all():
            matches.append({"name":m.full_name,
                            "username":m.username,
                            "image":m.image_url})

        return accepted_response(json.dumps(matches))



class GetCoincidences(APIView):
    
    def post(self,request,*args,**kwargs):
        try:            
            id_ = int(request.GET["id"])
            
            profile = Profile.objects.get(id=id_)
            search_pref = []
            size = 10

            for interest in profile.interests.all():
                search_pref.append(interest.name)

            # By default size is 5
            data = search_common_interests(search_pref,size,'es',0)
            

            max_cycles_allowed = 6
            # Avoid showing users already matched !
            # only filter if user has matches
            if profile.matches.all().count() > 0:
                for e in data:
                    for user in profile.matches.all():
                        if e['username'].lower() == user.username.lower():
                            data.remove(e) 
                            break
            
            return accepted_response(json.dumps({"results":data}))
            
        except:
            return failed_response("Any matches found")