from core.models import LANGUAGES
import json
from rest_framework.views import APIView
from users.models import *
from core.utils import accepted_response, failed_response, get_profile_by_id, is_lang_valid

class SetLanguage(APIView):
    def post(self,request,*arg,**kwargs):
        """
            Create a new lengauge
        """
        try:
            profile = get_profile_by_id(int(request.GET["id"]))
            lang = request.POST.get("lang")
            level = request.POST.get("level")

            if (is_lang_valid(lang) and int(level) <= 100):
                for e in profile.languages.all():
                    if e.name == lang:
                        return failed_response("Language already exists")

                lang_ = Languages.objects.create(name=lang,
                                                level=level)
                profile.languages.add(lang_)
                return accepted_response(json.dumps({lang_.id:lang_.name,"level":lang_.level}))
            else:
                return failed_response("Level provided is not under 100")
        except:
            return failed_response("Error adding the language")




class UpdateLanguageLevel(APIView):
    def post(self,request,*args,**kwargs):
        try:
            lang = Languages.objects.get(id=int(request.GET["lang"]))
            level = int(request.POST.get("level"))

            if level <= 100:
                lang.level = level

            return accepted_response({"level":level})
        except:
            return failed_response("Something went wrong")


class DeleteLanguage(APIView):
    def get(self,request,*arg,**kwargs):
        try:
            Languages.objects.get(id=request.GET["lang"]).delete()
            return accepted_response("Item deleted")
        except:
            return failed_response("Error deleting the language (maybe due to syntax error)")

class AllLanguages(APIView):
    def get(request,self,*args,**kwargs):
        try:
            # Show all accepted languages            
            return accepted_response(json.dumps(LANGUAGES))
        except:
            return failed_response("Problem while reading languages")


class GetPreferences(APIView):
    def get(self,request,*args,**kwargs):
        try:
            profile = get_profile_by_id(int(request.GET["id"]))
            languages = []
            interests = []
            for e in profile.interests.all():
                interests.append({e.id:e.name})
            for l in profile.languages.all():
                languages.append({l.id:l.name,"level":l.level})
            return accepted_response(json.dumps({
                                                "interests":interests,
                                                "languages":languages}))
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

            #Added to the profile 
            profile.interests.add(interest)
            return accepted_response(json.dumps({interest.id:interest.name}))
        except:
            return failed_response("Error adding the preference")

class DeletePreference(APIView):

    def get(self,request,*arg,**kwargs):
        try:
            pref_id = request.GET["preference"]
            Interest.objects.get(id=pref_id).delete()

            return accepted_response(json.dumps("Correctly deleted"))
        except:
            return failed_response("Error deleting the preference (maybe due to syntax error)")