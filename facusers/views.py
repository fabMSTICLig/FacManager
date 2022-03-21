import dateutil.parser
from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import render
from django.utils import timezone
from django.conf import settings
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework import filters

from facmanager.filters import IdsFilter

from .serializers import UserSerializer, UserPublicSerializer, NewUserSerializer, PasswordSerializer, OrganizationSerializer, OrganizationPublicSerializer, ProjectSerializer, LoginSerializer

from .models import Organization, Project
from .permissions import IsAdminOrIsSelf, IsMember, IsAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    search_fields = ('username', 'email', 'first_name', 'last_name')

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'retrieve', 'set_password']:
            permission_classes = [IsAdminOrIsSelf, IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(methods=['put'], detail=True, serializer_class=PasswordSerializer)
    def set_password(self, request, pk):
        """
        End point to change the password of a user
        """
        serializer = PasswordSerializer(data=request.data)
        user = get_user_model().objects.get(pk=pk)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Wrong password.']},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'status': 'password set'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)



    @action(methods=['post'], detail=False, serializer_class=NewUserSerializer)
    def create_user(self, request):
        """
        Special end point for creating user

        Only need first_name, last_name and email

        Generate a unique usermane and a password
        """
        serializer = NewUserSerializer(data=request.data)
        if serializer.is_valid():
            firstname = serializer.data.get('first_name')
            lastname = serializer.data.get('last_name')
            email = serializer.data.get('email')
            username = (lastname[:7]+firstname[0]).lower()
            count = 2
            while(get_user_model().objects.filter(username=username).exists()):
                username = (lastname[:7]+firstname[0]).lower()+str(count)
                count = count+1
            password = username[::-1]
            user = get_user_model().objects.create_user(username, email, password)
            user.last_name = lastname
            user.first_name = firstname
            user.save()
            serialized_class = UserSerializer(user)
            return Response(serialized_class.data, status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

class LogoutView(APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        logout(request)
        return Response(None, status=status.HTTP_205_RESET_CONTENT)

class RGPDAcceptView(APIView):
    """
    Endpoint to accept rgpd conditions
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if request.user.rgpd_accept is None and 'accept' in request.data:
            if request.data['accept']:
                request.user.rgpd_accept = timezone.now().date()
                request.user.save()
        return Response({"rgpd_accept": request.user.rgpd_accept})

    def get(self, request, format=None):
        return Response({"rgpd_accept": request.user.rgpd_accept})


class SelfView(APIView):
    def get(self, request, format=None):
        instance = UserSerializer(request.user, context={'request': request})
        return Response({"user": instance.data})

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return OrganizationSerializer
        else:
            #Hide contact to non-staff
            return OrganizationPublicSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'types']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(methods=['get'], detail=False)
    def types(self, request):
        """
        Return the organization types
        """
        return Response(dict((x, y) for x, y in settings.ORGANIZATION_TYPES), status=status.HTTP_200_OK)

class OldFilterBackend(filters.BaseFilterBackend):
    """
    Filter on date.
    """
    def filter_queryset(self, request, queryset, view):
        afterdate = request.query_params.get('afterdate', None)
        query=queryset
        try:
            if afterdate is not None:
                afterdate=dateutil.parser.parse(afterdate)
                query=query.filter(end_date__gte=afterdate)
        except:
            raise ParseError(detail="Wrong date format")
        return query



class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, OldFilterBackend, IdsFilter]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Project.objects.all()
        else:
            return self.request.user.projects.all()


    def get_permissions(self):
        if self.action in ['list', 'retreive']:
            permission_classes = [IsAuthenticated, IsMember]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
