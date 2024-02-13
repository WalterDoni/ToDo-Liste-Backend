
from django.shortcuts import render

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from todolist.models import TodoItem
from todolist.serializers import TodoItemSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
import json

class TodoItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        todos = TodoItem.objects.filter(author=request.user)
        serializers = TodoItemSerializer(todos, many=True)
        return Response(serializers.data)
  
  
  
#def createToDo(request):
    #if request.method == 'POST':
        #new_todo = TodoItem.objects.create(titel=)
        
  
  
  
  
  
    
class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        
  
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if username:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                return JsonResponse({'success': True, 'message': 'Benutzer erfolgreich erstellt'})
            except Exception as e:
                # Fehler bei der Benutzererstellung
                return JsonResponse({'success': False, 'message': str(e)})
        else:
            return JsonResponse({'success': False, 'message': 'Benutzername fehlt'})
    else:
        return HttpResponse("Nur POST-Anfragen werden unterstützt", status=405)


def deleteUser_view(request, username):
    try:
        user = User.objects.get(username=username)
        user.delete()
        return JsonResponse({"message": f"Der Benutzer {username} wurde erfolgreich gelöscht."}, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": f"Der Benutzer {username} existiert nicht."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Ein Fehler ist aufgetreten: {str(e)}"}, status=500)


def changeUsername_view(request, username, newUsername):
    try:
        user = User.objects.get(username=username)
        user.username = newUsername
        user.save()
        return JsonResponse({"message": f"Der Benutzername von {username} wurde erfolgreich auf {newUsername} geändert."}, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": f"Der Benutzer {username} existiert nicht."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Ein Fehler ist aufgetreten: {str(e)}"}, status=500)
