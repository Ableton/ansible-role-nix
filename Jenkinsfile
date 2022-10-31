library(identifier: 'ableton-utils@0.22', changelog: false)
library(identifier: 'groovylint@0.13', changelog: false)
library(identifier: 'python-utils@0.12', changelog: false)


devToolsProject.run(
  setup: { data ->
    // Temporary workaround for molecule's awful handling of roles and collections. It
    // insists on installing everything to ~/.cache/ansible-compat, which causes problems
    // on our CI system once it discovers that roles with different versions are there.
    sh 'rm -rf $HOME/.cache/ansible-compat'

    Object venv = virtualenv.createWithPyenv(readFile('.python-version'))
    venv.run('pip install -r requirements-dev.txt')
    data['collectionsPath'] = "${env.WORKSPACE}/.ansible/collections"
    venv.run('ansible-galaxy collection install' +
      " --collections-path ${data.collectionsPath}" +
      ' --requirements-file requirements.yml')
    data['rolesPath'] = "${env.WORKSPACE}/.ansible/roles"
    venv.run('ansible-galaxy install' +
      " --roles-path ${data.rolesPath}" +
      ' --role-file requirements.yml')
    dir('.ansible/roles') {
      // Create a symlink for the current role name in the roles path. This is necessary
      // because our CI system checks out all repositories to a directory named
      // "workspace", which confuses Molecule. Since Molecule determines the role's name
      // based on the current working directory, we need another way to tell it where to
      // find the role.
      sh "ln -s ../.. ${env.JENKINS_REPO_SLUG.split('/')[1]}"
    }
    data['venv'] = venv
  },
  test: { data ->
    parallel(failFast: false,
      'ansible-lint': {
        data.venv.run(
          label: 'ansible-lint',
          script: 'ansible-lint --strict --offline -c .ansible-lint.yml',
        )
      },
      groovylint: { groovylint.checkSingleFile(path: './Jenkinsfile') },
      molecule: {
        withEnv([
          "ANSIBLE_COLLECTIONS_PATH=${data.collectionsPath}",
          "ANSIBLE_ROLES_PATH=${data.rolesPath}",
        ]) {
          data.venv.run('molecule --debug test')
        }
      },
      yamllint: { data.venv.run('yamllint --strict .') },
    )
  },
  deployWhen: { devToolsProject.shouldDeploy(defaultBranch: 'main') },
  deploy: { data ->
    String versionNumber = readFile('VERSION').trim()
    version.tag(versionNumber)

    List repoSlugParts = params.JENKINS_REPO_SLUG.split('/')
    String repoOrg = repoSlugParts[0]
    String repoName = repoSlugParts[1]
    withCredentials([
      string(credentialsId: 'ansible-galaxy-api-key', variable: 'API_KEY')
    ]) {
      data.venv.run(
        label: 'Publish to Ansible Galaxy',
        script: "ansible-galaxy role import --branch ${versionNumber}" +
          ' --api-key $API_KEY' +  // avoid exposing the credential in the build log
          " ${repoOrg} ${repoName}",
      )
    }
  },
)
