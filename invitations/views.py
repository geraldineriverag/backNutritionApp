from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Invitation
from .serializers import InvitationSerializer

class InvitationViewSet(viewsets.ModelViewSet):
    """
    Gestión de invitaciones.
    - CRUD normal para nutricionistas.
    - Acción extra `accept` para que un paciente acepte su invitación.
    """
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Nutricionistas sólo ven sus invitaciones
        user = self.request.user
        if getattr(user, 'role', None) == 'nutricionista' and hasattr(user, 'nutritionist_profile'):
            return Invitation.objects.filter(nutritionist=user.nutritionist_profile)
        return Invitation.objects.none()

    @action(detail=False, methods=['post'], url_path='accept')
    def accept_invitation(self, request):
        """
        POST /api/invitations/accept/   body: { token: string }
        El paciente autenticado que llama a esta ruta asociará su perfil al nutritionist.
        """
        token = request.data.get('token', '').strip()
        user  = request.user

        # Buscar invitación no aceptada, emitida al email de este usuario
        inv = Invitation.objects.filter(
            token=token,
            email=user.email,
            accepted=False
        ).first()
        if not inv:
            return Response(
                {"detail": "Invitación inválida o ya usada."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Marca aceptada y asocia al usuario como paciente
        inv.accept(user)
        return Response(InvitationSerializer(inv).data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        # Esto es lo importante para que el serializer vea `request`
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    def perform_create(self, serializer):
        # 1) Crear la invitación (que internamente genera token y asigna nutritionist)
        invitation = serializer.save()

        # 2) Enviar correo al paciente
        subject = f"Invitación de {invitation.nutritionist.user.first_name}"
        link = f"https://tu-app.com/accept?token={invitation.token}"
        message = (
            f"Hola,\n\n"
            f"Has sido invitado por {invitation.nutritionist.user.first_name} "
            f"a formar parte de su lista de pacientes.\n\n"
            f"Pulsa aquí para aceptar: {link}\n\n"
            "Si no tienes nuestra app, instala desde ...\n\n"
            "¡Gracias!"
        )
        send_mail(
            subject,
            message,
            'no-reply@tuapp.com',
            [invitation.email],
            fail_silently=False,
        )