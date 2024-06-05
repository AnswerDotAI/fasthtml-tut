# fasthtml-tut

Code to go with beginner FastHTML tutorial. First install fasthtml:

    pip install -U python-fasthtml

Make sure you've installed the `railway` CLI, and logged in with:

    railway login

Then, to deploy an app, cd to the directory, and run (replacing `NAME` with your preferred app name):

```sh
railway init -n NAME
railway up -c
railway domain
fh_railway_link
railway volume add -m /app/data
```

There is a shell script `deploy.sh` in the current directory with those lines, so a shortcut is to just call it from the directory with the app:

    ../deploy.sh

