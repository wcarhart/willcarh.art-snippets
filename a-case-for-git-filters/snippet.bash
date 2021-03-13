#!/bin/bash

# WARNING: this script assumes your local username is the same as your GitHub username

# create dummy repository
mkdir ~/MyCoolApp
cd !$
git init

# create dummy application
echo -e 'const DBNAME = "MyCoolApp_DB"\nconst DBPASS = "pA$$w0rD"' > app.js

# create new Git filter 'resolveSecret'
git config --global filter.resolveSecret.smudge "sed 's/SMUDGED_DATABASE_PASSWORD/pA$$w0rD/g'"
git config --global filter.resolveSecret.clean "sed 's/pA$$w0rD/SMUDGED_DATABASE_PASSWORD/g'"

# register 'resolveSecret' with current repository
echo 'app.js filter=resolveSecret' > .gitattributes

# commit code
git status
git add -A
git commit -m 'Initial commit'

# create the remote
gh repo create --public $(basename "$(pwd)")

# confirm it added remote 'origin' to our local repository
git remote --verbose

# gh sets up remotes using HTTPS, if we want to use SSH we'll have to reconfigure 'origin'
git remote rm origin
git remote add origin git@github.com:$(whoami)/$(basename "$(pwd)").git
git remote --verbose

# push to remote
git push -u origin master

# open remote in browser
if [[ "$(uname -s)" == 'Darwin' ]] ; then open "https://github.com/$(whoami)/$(basename "$(pwd)")" ; fi
