"""
Principals — representan la identidad del usuario que ejecuta una acción.

V1: AnonymousPrincipal (sin auth, autoriza todo).
V2: Reemplazar por AuthenticatedPrincipal sin cambiar firmas de servicio.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AnonymousPrincipal:
    """Principal sin autenticación. Autoriza todas las operaciones en V1."""

    identity: str = "anonymous"
