library(identifier: 'ableton-utils@0.28', changelog: false)
library(identifier: 'groovylint@0.15', changelog: false)
library(identifier: 'python-utils@0.13', changelog: false)


devToolsProject.run(
  defaultBranch: 'main',
  setup: { data ->
    Object venv = pyenv.createVirtualEnv(readFile('.python-version').trim())
    venv.inside {
      sh 'pip install -r requirements-dev.txt'
      ansibleUtils.galaxyInstall()
    }
    data['venv'] = venv
  },
  test: { data ->
    data.venv.inside {
      parallel(
        'ansible-lint': { ansibleUtils.ansibleLint() },
        groovylint: { groovylint.checkSingleFile(path: './Jenkinsfile') },
        molecule: { ansibleUtils.molecule() },
        yamllint: { sh 'yamllint --strict .' },
      )
    }
  },
  deploy: { data ->
    data.venv.inside { ansibleUtils.publishRole('ansible-galaxy-api-key') }
  },
)
