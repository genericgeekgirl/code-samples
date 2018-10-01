To run the API, you'll need Python and Flask (http://flask.pocoo.org/).

Then `python app.py` which will run it on http://localhost:5000/

endpoints.py contains the code to run from a commandline without a webserver

# Original README

At Tidelift, one of the things that we make heavy use of is showing people
metadata about the software packages that they use. We have collected a lot of
this information in a database that we have and other pieces are instead
available via public APIs.

For this exercise, we want you to write an API server in the language and
framework of your choice to expose some information about javascript packages.
There are two API endpoints.

# First endpoint

The first endpoint should accept GET requests to urls of the form
_/package/health/:packagename/:version_ where _:packagename_ is the name of
the package (something like axios, firebase, bulma, github-api, etc) and
:version is the specific version to get data about. The response shoudl be a
json dictionary for that package containing information about the license and
security vulnerabilities in that version of that package. An example output to
/package/health/dummy/0.9 should look like the following

```json
{
    "name": "dummy",
    "version": "0.9",
    "license": "MIT",
    "vulnerabilities": [
        {
            "id": "v2017-001",
            "description": "this is a dummy cve",
            "created": "2017-09-01T14:32:93Z"
        }
    ]
}
```

Rather than requiring a lookup in a database or an API call, we have provided
you with two CSV files that contain information that can be used for your API.

* licenses.csv - this is a text file where each line refers to a package.
  Fields in the file are the package name and the license.
* vulnerabilities.csv - this is a text file where each line refers to a single
  vulnerability. Fields are vulnerability id, package name, package version,
  description, and a created timestamp

# Second endpoint

The second endpoint should accept GET requests to urls of the form
_/package/releases/:packagename_ where _:packagename_ is again the name of the
package. An example output to /package/releases/tiny-tarball should look like
the following

```json
{
    "name": "tiny-tarball",
    "latest": "1.0.0",
    "releases": [
        "1.0.0"
    ]
}
```

You can get this information by making an API call to the NPM registry which
is available with a GET request to _https://registry.npmsjs.org/:packagename_.
That call will return JSON as described in depth in [their
documentation]
(https://github.com/npm/registry/blob/master/docs/responses/package-metadata.md).
In your response, releases should be a list of the
versions available from npm (from the _versions_ in the response from npmjs)
and latest should be the most recently published version based on looking at
the values of the _time_ dictionary in the response from npmjs.

# A couple logistical notes...

When done, please provide us with either a link to a private GitHub repository or an
archive of your code along with instructions on how to run it.

If you have *any* questions, please don't hesitate to ask much as you would if we were
sitting next to each other working on this. A good rule of thumb is that if
you're stuck for fifteen minutes, that's probably time to ask for a
clarification!

Thank you for your time; we're grateful for the opportunity to get to know you better.
