<!-- write about how to create their own pipenv, then install flask and python -->

# Database Management Application Prototype
The role of this small web relation management application is to be a standard where the student may extend the capabilities integrating more relational operations. The view of the application is written in a compact view (front-end) library `React`, in `TypeScript`. Feel free to check the *detailed comments* on the code to get to know what it does. The **main part**, the back-end operations are written in Python, using the library `flask`, and PostgresQL is used as the database engine. The directory structure and program architecture is given below and to activate/setup the environment, follow the instructions below.
## Directory Structure
1. `docker-compose.yaml` - Docker compose file used to build the Postgres environment and its admin interface
2. `app.py` - codebase of the backend API and database integration. SQL statements to be written here
3. `src/api.ts` - codebase communicating the view with the main api (namely functionalities of `app.py`)
4. `App.tsx` - main view file where the relation data gathered from the database is rendered
5. `components/<View>.tsx` - auxiliary view components used in `App.tsx` to render the relation and the editor application structurally (check the comments in the files for a detailed cover)
### Miscellaneous (you won't need to modify manually):
6. `main.tsx` and `index.css` - entrance point files not to be modified: all content of `App.tsx` and `App.scss` are compiled into them respectively
7. Files including `vite` - config files for a fast build tool Vite 
8. `tsconfig.json` - compiler configuration for  TypeScript
9. `package.json` - includes names and versions of the necessary view libraries used in the application
10. `.gitignore`; `index.html`; `node_modules` - keeps unnecessary files away from version control; main entry point for the browser; folder storing necessary installed JavaScript libraries 