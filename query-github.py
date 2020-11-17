import requests
import json
import sys
import os

response = requests.get('https://api.github.com/users/josephsamela/repos?per_page=100')

repos = json.loads(response.text)

if 'message' in repos:
    if 'exceeded' in repos['message']:
        print('Request limit exceeded. Github has cut you off.')
        sys.exit()

for repo in repos:
    if not repo['fork']:
        date = repo['created_at'][0:10]
        url = repo['html_url']
        name = repo['name']
        full_name = repo['full_name']
        default_branch = repo['default_branch']

        # Get readme text
        filenames = ['readme.md', 'README.md']
        for filename in filenames:
            readme = requests.get('https://raw.githubusercontent.com/'+full_name+'/'+default_branch+'/'+filename)
            if readme.status_code == 404:
                continue
            else:
                break

        # skip repo if no readme
        if readme.status_code == 404:
            continue

        print('Downloading ... '+date+'.'+name)

        readme_absolute = ''
        first = True
        for line in readme.text.splitlines():
            # Handle images, convert relative paths to absolute
            if '![' in line:
                path = line.split('](')[1].split(')')[0]
                if 'http' in path:
                    image = line
                else:
                    if './' in path:
                        path = path[2:]
                    line = '![](https://raw.githubusercontent.com/'+full_name+'/'+default_branch+'/'+path+')'
            # Handle codeblocks, replace blank "```" with "```abc"
            elif '```' in line:
                if first:
                    if '```' == line:
                        line = '```abc'
                    first = False
                else:
                    first = True


            readme_absolute += line+'\n'

        # write readme to file
        with open('pages/'+date+'.'+name+'.md', 'w')  as f:
            f.write('<br>[See project on github!]('+url+')\n\n')
            f.write(readme_absolute)
