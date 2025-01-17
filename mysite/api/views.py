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
                "user2": data.get('user2'),
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

@api_view(['POST'])
def CreateMessage(request):
    if request.method == 'POST':
        try:
            data = request.data 
            messageID = data.get('id')

            message_body = {
                "text": data.get('text'),
                "sender": data.get('sender'),
                "id": messageID,
            }
            serializer = MessageSerializer(data=message_body)

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
    else:
        # Return a 405 if it's not a POST request
        return Response(
            {"detail": "Method not allowed. Only POST"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

