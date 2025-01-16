from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import ConversationSerializer
from .models import UserConversation
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

@api_view(['POST'])
def CreateConversation(request):
    if request.method == 'POST':
        try:
            data = request.data
            conversationID = data.get('id')

            conversation_body = {
                "user1": data.get('user1'),
                "user2": data.get('user2'),  # Dynamically pulled from request
                "id": conversationID,
            }

            serializer = ConversationSerializer(data=conversation_body)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"Validation Errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Log the error
            logger.error(f"An error occurred: {e}", exc_info=True)
            return Response(
                {"detail": "An unexpected error occurred."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
