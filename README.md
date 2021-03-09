# Moment
Moment is a prototype framework with the goal of connecting citizen scientists with software experience with scientific researchers projects.
A key goal is to enable building and maintaining of software and services, and completion of applied ML projects jointly between academics and contributors from outside academia


[Visit Moment](https://blaiszik.github.io/moment/)




# Getting Started
To start a new project:
### 1. Clone a template repository
**Software Template:** `git clone https://github.com/blaiszik/moment-software`

**ML Template:** `git clone https://github.com/blaiszik/moment-ml`

### 2. Add Your Project
Submit your proposed project by issuing a pull request to this repository adding your new project repository to the file located in this repository at 
`moment/data/input/projects.jsonl`

This input currently accepts the following keys:

`project`: This maps to a user or organization in Github

`repo`: This maps to an individual repository in Github

`path`: Lists the path the Moment service should aggregate project metadata (e.g., credits, papers, etc.) from

`description`: A free text description of the project to help others find and understand the scope of the project

`contacts`: A list of objects including a contact `name` and `email` to be associated with project. This can for example be the PI.

`credits`: Credits is an object that is added to a project by the PR reviewers. Please do not include it in your submission.

**Please note this should be a single line in the commit**
To register a project at the following location `https://github.com/blaiszik/moment` with the default directory `.moment`
```json
{
  "project":"blaiszik", 
   "repo":"moment-ml",
   "path":".moment", 
   "description": "My project description ...",
   "contacts":[{"name":"Albert Einstein", "email":"albert@ethz.cz"}, {"name":"Ada Lovelace", "email":"adalovelace@gmail.com"}]
}
```

# Aggregated Information
Moment aggregates the following information from each project
1. Project descriptions
2. Project issues (currently via Github Issues)
3. Assigned credits
4. Academic research outputs (currently, we support papers, presentations, books, and more in BibTeX format)


# Support
Currently bootstrapped in spare cycles by researchers from the University of Chicago, Argonne National Laboratory, NIST, and the University of Wisconsin-Madison.


# Contributors
