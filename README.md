# Lumino

**Lumino** es un proyecto web desarrollado con Django para la gestión académica. La aplicación permite al alumnado matricularse en distintos módulos, al profesorado añadir contenidos a esos módulos y calificar las materias de forma centralizada y eficiente.

## Características

- Gestión de usuarios (profesorado y alumnado).
- Matrícula en módulos y calificación de materias.
- Generación dinámica de certificados en PDF.
- Gestión de contenidos por módulo, incluyendo lecciones y notas.
- Interfaz de administración basada en Django Admin.

## Puesta en marcha

Sigue los pasos a continuación para iniciar el proyecto:

1. Crea un entorno virtual:
   ```bash
   just create-venv
   source .venv/bin/activate
   ```
2. Configura el proyecto:
   ```bash
   just setup
   ```

### ¿Qué sucede durante la configuración?

- Se crea un entorno virtual en la carpeta `.venv`.
- Se instalan las dependencias necesarias.
- Se inicializa un proyecto Django en la carpeta `main`.
- Se aplican las migraciones iniciales.
- Se crea un superusuario con credenciales predeterminadas: `admin` / `admin`.

## Aplicaciones incluidas

El proyecto utiliza una arquitectura modular con las siguientes aplicaciones:

- **accounts**: Gestión de autenticación.
- **shared**: Componentes compartidos entre aplicaciones.
- **users**: Gestión de usuarios y perfiles.
- **subjects**: Gestión de módulos, lecciones y calificaciones.

## Modelos principales

### `subjects.Subject`

- `code` (str): Código del módulo.
- `name` (str): Nombre del módulo.
- `teacher` (fk → User): Profesor asignado.
- `students` (m2m → User): Alumnado matriculado.

### `subjects.Lesson`

- `subject` (fk → Subject): Módulo al que pertenece.
- `title` (str): Título de la lección.
- `content` (str, opcional): Contenido de la lección.

### `subjects.Enrollment`

- `student` (fk → User): Alumno/a matriculado/a.
- `subject` (fk → Subject): Módulo en el que está matriculado/a.
- `enrolled_at` (date): Fecha de matrícula.
- `mark` (int, opcional): Nota asignada.

### `users.Profile`

- `user` (o2o → User): Usuario asociado.
- `role` (enum): Rol del usuario (por defecto, STUDENT).
- `avatar` (image, opcional): Imagen del perfil.
- `bio` (str, opcional): Descripción del perfil.

## Administración

Los siguientes modelos son gestionables desde la interfaz administrativa de Django:

- `subjects.Subject`
- `subjects.Lesson`
- `subjects.Enrollment`
- `users.Profile`

## Contribuciones

¡Las contribuciones son bienvenidas! Sigue estos pasos para contribuir:

1. Realiza un fork del repositorio.
2. Crea una rama para tu contribución:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Realiza los cambios necesarios y realiza un commit.
4. Envía un pull request a la rama principal.

## Licencia

Este proyecto está licenciado bajo la licencia **CC BY 4.0**. Consulta el archivo [LICENSE](LICENSE) para más información.

## Agradecimientos

Desarrollado como parte del curso "Aprende Python comiendo pipas" de **pypas.es**.
