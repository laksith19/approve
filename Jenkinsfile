def dists = ['stretch']

def parallelBuilds = dists.collectEntries { dist ->
  [dist, {
    stage("build-${dist}") {
      sh 'make clean'
      sh "make package_${dist}"
      archiveArtifacts artifacts: "dist_${dist}/*"
    }
  }]
}


pipeline {
  // TODO: Make this cleaner: https://issues.jenkins-ci.org/browse/JENKINS-42643
  triggers {
    upstream(
      upstreamProjects: (env.BRANCH_NAME == 'master' ? 'ocflib/master' : ''),
      threshold: hudson.model.Result.SUCCESS,
    )
  }

  agent {
    label 'slave'
  }

  options {
    ansiColor('xterm')
    timeout(time: 1, unit: 'HOURS')
    timestamps()
  }

  stages {
    stage('check-gh-trust') {
      steps {
        checkGitHubAccess()
      }
    }

    stage('test') {
      steps {
        sh 'make test'
      }
    }

    stage('parallel-builds') {
      steps {
        script {
          parallel parallelBuilds
        }
      }
    }

    // Upload packages in series instead of in parallel to avoid a race
    // condition with a lock file on the package repo
    stage('upload-packages') {
      when {
        branch 'master'
      }
      agent {
        label 'deploy'
      }
      steps {
        script {
          for(dist in dists) {
            stage("upload-${dist}") {
              uploadChanges(dist, "dist_${dist}/*.changes")
            }
          }
        }
      }
    }
  }

  post {
    failure {
      emailNotification()
    }
    always {
      node(label: 'slave') {
        ircNotification()
      }
    }
  }
}

// vim: ft=groovy
