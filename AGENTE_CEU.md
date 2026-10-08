# Agente de calendario CEU - Grupo B

Suscripción permanente: https://rafagonzalovilla-cyber.github.io/calendario/calendario-ceu.ics

Origen identificado:
https://ceu.blackboard.com/ultra/courses/_363043_1/document/_4726501_1?view=content&state=view

**Estado (fase 1):** GitHub Actions revisa diariamente la estructura del calendario y comprueba si la publicación de Blackboard es accesible desde sus servidores. Consulta los resultados en Actions > CEU - comprobar calendario y acceso Blackboard > Summary.

**NO está activada la importación automática de PDF.** Abrir Blackboard sin una nueva contraseña desde SharePoint solo implica inicio de sesión único en el navegador del alumno, no autoriza a GitHub Actions a iniciar sesión por su cuenta.

Próxima fase:
1. Establecer método autorizado de descarga automática, preferentemente API REST habilitada por CEU o acceso con sesión local en Windows.
2. Construir y probar el parser de PDF/Excel de la plantilla del máster, teniendo en cuenta grupo B y sesiones comunes.
3. Comparar versiones de forma segura y actualizar este mismo archivo ICS manteniendo UIDs estables.
4. Habilitar la publicación automática únicamente cuando las tres comprobaciones anteriores pasen.

No incluyas contraseñas, cookies, tokens ni documentos privados en este repositorio público.
