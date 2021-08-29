import json
from rest_framework.views import APIView
from users.models import *
from core.utils import accepted_response, failed_response, get_profile_by_id

class SetLanguage(APIView):
    def post(self,request,*arg,**kwargs):
        try:
            return accepted_response(json.dumps({1,"es"}))
        except:
            return failed_response("Error adding the language")

class DeleteLanguage(APIView):
    def post(self,request,*arg,**kwargs):
        try:
            return accepted_response("Item deleted")
        except:
            return failed_response("Error deleting the language")



class GetPreferences(APIView):
    def get(self,request,*args,**kwargs):
        try:
            profile_id = request.GET["id"]
            profile = Profile.objects.get(id=profile_id)
            data = []
            for e in profile.interests.all():
                data.append(e)
            return accepted_response(json.dumps(data))
        except:
            return failed_response("Not found preferences")


class SetPreference(APIView):
    """
        @param id
        @param preference
    """
    def post(self,request,*arg,**kwargs):
        try:
            # Return the id,name
            profile = get_profile_by_id(int(request.GET["id"]))
            interest_name = request.POST.get("preference")
            interest = Interest.objects.create(name=interest_name)
        
            return accepted_response(json.dumps({interest.id:interest.name}))
        except:
            return failed_response("Error adding the preference")

class DeletePreference(APIView):
    def post(self,request,*arg,**kwargs):
        try:
            return accepted_response(json.dumps("Correctly deleted"))
        except:
            return failed_response("Error deleting the preference")