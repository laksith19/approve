node('slave') {
    step([$class: 'WsCleanup'])

    stage('check-out-code') {
        dir('src') {
            checkout scm
        }
    }

	stage('test') {
		dir('src') {
			sh 'make test'
		}
	}

    stash 'src'
}


def dists = ['jessie', 'stretch']
for (def i = 0; i < dists.size(); i++) {
    def dist = dists[i]
    stage name: "build-${dist}"

    node('slave') {
        step([$class: 'WsCleanup'])
        unstash 'src'

        dir('src') {
            sh 'make clean'
            sh "make package_${dist}"
            sh "mv dist dist_${dist}"
            archiveArtifacts artifacts: "dist_${dist}/*"
        }

        stash 'src'
    }

    if (env.BRANCH_NAME == 'master') {
        stage name: "upload-${dist}"

        build job: 'upload-changes', parameters: [
            [$class: 'StringParameterValue', name: 'path_to_changes', value: "dist_${dist}/*.changes"],
            [$class: 'StringParameterValue', name: 'dist', value: dist],
            [$class: 'StringParameterValue', name: 'job', value: env.JOB_NAME.replace('/', '/job/')],
            [$class: 'StringParameterValue', name: 'job_build_number', value: env.BUILD_NUMBER],
        ]
    }
}

// vim: ft=groovy
