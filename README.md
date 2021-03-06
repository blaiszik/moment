# Moment
Moment is a prototype framework with the goal of connecting citizen scientists with software experience with scientific researchers projects.
A key goal is to enable building and maintaining of software and services, and completion of applied ML projects jointly between academics and contributors from outside academia


# Getting Started
To start a new project:
### Clone the template repository
`git clone https://github.com/blaiszik/moment1.git`

### Fill in the project description
Template TBD

### Submit
Submit your proposed project by issuing a pull request to this repository adding your new project repository to the file located in this repository at 
`moment/data/input/projects.jsonl`

This input currently accepts the following keys:

`project`: This maps to a user or organization in Github

`repo`: This maps to an individual repository in Github

`path`: Lists the path the Moment serviec should aggregate project metadata (e.g., credits, papers, etc.) from

`description`: A free text description of the project to help others find and understand the scope of the project


**Please note this should be a single line in the commit**
To register a project at the following location `https://github.com/blaiszik/moment` with the default directory `.moment`
```json
{
  "project":"blaiszik", 
   "repo":"moment-ml",
   "path":".moment", 
   "description": "My project description"
}
```

# Support



# Contributors
