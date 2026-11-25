import hmac
import os
from datetime import datetime
import pyotp
from pyotp.totp import TOTP
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from werkzeug.security import check_password_hash

MFA_TOKEN_VALIDADE_SEGUNDOS = 300
MFA_ISSUER = "PI Backend"


class AuthService:

    def __init__(self, repository):
        self.repository = repository

    def login(self, dados):
        email = dados.get("email")
        senha = dados.get("senha")

        if not email or not senha:
            raise ValueError("Email e senha são obrigatórios")

        usuario = self.repository.buscar_por_email(email)

        if not usuario or not check_password_hash(usuario.senha_hash, senha):
            raise ValueError("Email ou senha inválidas.")

        return usuario

    def _serializer(self):
        secret_key = os.getenv("JWT_SECRET_KEY")
        if not secret_key:
            raise ValueError("JWT_SECRET_KEY não está configurada.")
        return URLSafeTimedSerializer(secret_key, salt="mfa-login")

    def gerar_mfa_token(self, usuario):
        return self._serializer().dumps({"uid": usuario.id})

    def verificar_login_mfa(self, dados):
        mfa_token = dados.get("mfa_token")
        codigo = dados.get("codigo")

        if not mfa_token or not codigo:
            raise ValueError("mfa_token e codigo são obrigatórios.")

        try:
            payload = self._serializer().loads(
                mfa_token, max_age=MFA_TOKEN_VALIDADE_SEGUNDOS
            )
        except SignatureExpired:
            raise ValueError("Sessão de MFA expirada. Faça login novamente.")
        except BadSignature:
            raise ValueError("mfa_token inválido.")

        usuario = self.repository.buscar_por_id(payload["uid"])

        if not usuario or not usuario.mfa_ativo:
            raise ValueError("MFA não está ativo para este usuário.")

        if not self._validar_codigo(usuario, codigo):
            self.repository.rollback()
            raise ValueError("Código inválido ou expirado.")

        self.repository.commit()
        return usuario

    def iniciar_mfa(self, usuario_id):
        usuario = self._buscar_usuario(usuario_id)

        if usuario.mfa_ativo:
            raise ValueError(
                "MFA já está ativo. Desative antes de gerar um novo segredo."
            )

        usuario.mfa_secret = pyotp.random_base32()
        usuario.mfa_ultimo_passo = None
        self.repository.atualizar(usuario)
        self.repository.commit()

        uri = TOTP(usuario.mfa_secret).provisioning_uri(
            name=usuario.email, issuer_name=MFA_ISSUER
        )
        return {"secret": usuario.mfa_secret, "otpauth_uri": uri}

    def ativar_mfa(self, usuario_id, dados):
        usuario = self._buscar_usuario(usuario_id)
        codigo = dados.get("codigo")

        if usuario.mfa_ativo:
            raise ValueError("MFA já está ativo.")
        if not usuario.mfa_secret:
            raise ValueError("Gere o segredo primeiro em /api/auth/mfa/setup.")
        if not codigo:
            raise ValueError("codigo é obrigatório.")

        if not self._validar_codigo(usuario, codigo):
            self.repository.rollback()
            raise ValueError("Código inválido ou expirado.")

        usuario.mfa_ativo = True
        self.repository.atualizar(usuario)
        self.repository.commit()

    def desativar_mfa(self, usuario_id, dados):
        usuario = self._buscar_usuario(usuario_id)
        senha = dados.get("senha")
        codigo = dados.get("codigo")

        if not usuario.mfa_ativo:
            raise ValueError("MFA não está ativo.")
        if not senha or not codigo:
            raise ValueError("senha e codigo são obrigatórios.")
        if not check_password_hash(usuario.senha_hash, senha):
            raise ValueError("Senha inválida.")
        if not self._validar_codigo(usuario, codigo):
            self.repository.rollback()
            raise ValueError("Código inválido ou expirado.")

        usuario.mfa_ativo = False
        usuario.mfa_secret = None
        usuario.mfa_ultimo_passo = None
        self.repository.atualizar(usuario)
        self.repository.commit()

    def _buscar_usuario(self, usuario_id):
        usuario = self.repository.buscar_por_id(int(usuario_id))
        if not usuario:
            raise ValueError("Usuário não encontrado.")
        return usuario

    def _validar_codigo(self, usuario, codigo):
        codigo = str(codigo).strip()
        if not codigo.isdigit() or len(codigo) != 6:
            return False

        totp = TOTP(usuario.mfa_secret)
        passo_atual = totp.timecode(datetime.now())
        ultimo = usuario.mfa_ultimo_passo or 0

        for passo in (passo_atual - 1, passo_atual, passo_atual + 1):
            if passo <= ultimo:
                continue
            if hmac.compare_digest(totp.generate_otp(passo), codigo):
                usuario.mfa_ultimo_passo = passo
                self.repository.atualizar(usuario)
                return True
        return False
