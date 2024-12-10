from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Tool, History
from .serializers import ToolSerializer
from .agent_service import process_user_input

import uuid

class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer

    
    # def post(self, request):
    #     serializer = ToolSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"message": "Tool added successfully"}, status=201)
    #     return Response(serializer.errors, status=400)


class AgentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user  # 当前登录用户
        session_id = request.data.get('session_id')  # 获取会话 ID
        user_input = request.data.get('query', '').strip()  # 获取用户输入

        if not user_input:
            return Response({"error": "Query is required"}, status=400)

        if not session_id:
            # 如果没有会话 ID，生成新的会话 ID
            session_id = str(uuid.uuid4())

        if not user_input:
            return Response({"error": "Query is required"}, status=400)

        response = process_user_input(user.id, session_id, user_input)
        return Response({"response": response})
    
    
class SessionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        user = request.user
        try:
            history = History.objects.get(user=user, session_id=session_id)
            return Response(history.history_data)
        except History.DoesNotExist:
            return Response({"error": "Session not found"}, status=404)