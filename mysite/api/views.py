from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import ConversationSerializer
from .models import UserConversation
# Create your views here.


@api_view(['POST'])
def CreateConversation(request):
	
	if request.method == 'POST':
		try:
			data = request.data

			conversationID = data.get('id')

			conversation_body = {
				"user1": request.user.id,
                "user2": "hello",
				"id": conversationID,
			}

			serializer = ConversationSerializer(data=conversation_body)

			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				print_error(serializer.errors, False)
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			print_error(e, True)
			return Response(status=status.HTTP_400_BAD_REQUEST)
	return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
