library(identifier: 'ableton-utils@0.22', changelog: false)
library(identifier: 'groovylint@0.13', changelog: false)
library(identifier: 'python-utils@0.13', changelog: false)


devToolsProject.run(
  setup: { data ->
    Object venv = pyenv.createVirtualEnv(readFile('.python-version'))
    venv.run('pip install -r requirements-dev.txt')
    data['venv'] = venv
  },
  test: { data ->
    data.venv.inside {
      parallel(
        'ansible-lint': {
          sh(
            label: 'ansible-lint',
            script: 'ansible-lint --strict --offline -c .ansible-lint.yml',
          )
        },
        groovylint: { groovylint.checkSingleFile(path: './Jenkinsfile') },
        molecule: { ansibleUtils.molecule() },
        yamllint: { sh 'yamllint --strict .' },
      )
    }
  },
  deployWhen: { devToolsProject.shouldDeploy(defaultBranch: 'main') },
  deploy: { data ->
    data.venv.inside { ansibleUtils.publishRole('ansible-galaxy-api-key') }
  },
)
