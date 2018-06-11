# About ictmpl

This script allows a create new project using a ready-made templates.

You can use template on local machine or repositories.

By default it looks for a name of template in the 
[official repository](https://github.com/ictmpl)


# Installing

    pip install ictmpl
    
or globally:

    sudo -H pip install ictmpl


# Usage

## create

Create new project by template

`ictmpl create <project_path> <template_name>`

#### Params:

* **project_path** - Path to new project directory
* **template_name** - Name of template / link to git repository / local path
    
#### Examples:

`ictmpl create flaskproject flask-blank`
    
`ictmpl create myproject ../my-local-template/`
    
`ictmpl create /var/www/myproject https://github.com/ictmpl/flask-blank.git`
    
