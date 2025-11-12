"""
Script para crear tipos de usuario por defecto en el sistema de post-ventas.
Ejecutar: python manage.py shell
Luego: exec(open('crear_tipos_usuario.py').read())
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_postventa.settings')
django.setup()

from postventa.models import TipoUsuario

def crear_tipos_usuario_defaults():
    """Crear tipos de usuario por defecto"""
    
    # 1. Revisor - Solo lectura
    revisor, created = TipoUsuario.objects.get_or_create(
        nombre='Revisor',
        defaults={
            'nivel_acceso': 'revisor',
            'descripcion': 'Usuario que solo puede revisar las post-ventas sin realizar modificaciones. Ideal para auditores o supervisores que necesitan visualizar la información.',
            'puede_crear_postventa': False,
            'puede_ver_todas_postventas': True,
            'puede_editar_todas_postventas': False,
            'puede_eliminar_todas_postventas': False,
            'puede_editar_propias_postventas': False,
            'puede_eliminar_propias_postventas': False,
            'puede_gestionar_usuarios': False,
            'puede_gestionar_comites': False,
            'activo': True,
        }
    )
    if created:
        print("✅ Creado tipo 'Revisor'")
    else:
        print("ℹ️  Tipo 'Revisor' ya existe")

    # 2. Usuario Básico
    usuario_basico, created = TipoUsuario.objects.get_or_create(
        nombre='Usuario Básico',
        defaults={
            'nivel_acceso': 'usuario',
            'descripcion': 'Usuario estándar que puede gestionar únicamente sus propias post-ventas. Perfil ideal para usuarios finales.',
            'puede_crear_postventa': True,
            'puede_ver_todas_postventas': False,
            'puede_editar_todas_postventas': False,
            'puede_eliminar_todas_postventas': False,
            'puede_editar_propias_postventas': True,
            'puede_eliminar_propias_postventas': True,
            'puede_gestionar_usuarios': False,
            'puede_gestionar_comites': False,
            'activo': True,
        }
    )
    if created:
        print("✅ Creado tipo 'Usuario Básico'")
    else:
        print("ℹ️  Tipo 'Usuario Básico' ya existe")

    # 3. Supervisor
    supervisor, created = TipoUsuario.objects.get_or_create(
        nombre='Supervisor',
        defaults={
            'nivel_acceso': 'supervisor',
            'descripcion': 'Usuario con permisos extendidos que puede ver todas las post-ventas pero solo editar las propias. Ideal para coordinadores.',
            'puede_crear_postventa': True,
            'puede_ver_todas_postventas': True,
            'puede_editar_todas_postventas': False,
            'puede_eliminar_todas_postventas': False,
            'puede_editar_propias_postventas': True,
            'puede_eliminar_propias_postventas': True,
            'puede_gestionar_usuarios': False,
            'puede_gestionar_comites': False,
            'activo': True,
        }
    )
    if created:
        print("✅ Creado tipo 'Supervisor'")
    else:
        print("ℹ️  Tipo 'Supervisor' ya existe")

    # 4. Administrador de Post-ventas
    admin_postventas, created = TipoUsuario.objects.get_or_create(
        nombre='Administrador de Post-ventas',
        defaults={
            'nivel_acceso': 'administrador',
            'descripcion': 'Usuario con control total sobre las post-ventas pero sin permisos de gestión de usuarios.',
            'puede_crear_postventa': True,
            'puede_ver_todas_postventas': True,
            'puede_editar_todas_postventas': True,
            'puede_eliminar_todas_postventas': True,
            'puede_editar_propias_postventas': True,
            'puede_eliminar_propias_postventas': True,
            'puede_gestionar_usuarios': False,
            'puede_gestionar_comites': True,
            'activo': True,
        }
    )
    if created:
        print("✅ Creado tipo 'Administrador de Post-ventas'")
    else:
        print("ℹ️  Tipo 'Administrador de Post-ventas' ya existe")

    print("\n🎯 Tipos de usuario creados correctamente!")
    print("📋 Resumen:")
    print("   • Revisor: Solo puede VER todas las post-ventas")
    print("   • Usuario Básico: Gestiona solo sus propias post-ventas")
    print("   • Supervisor: Ve todas, edita solo las propias")
    print("   • Administrador de Post-ventas: Control total")

if __name__ == '__main__':
    crear_tipos_usuario_defaults()