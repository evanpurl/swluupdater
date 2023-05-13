pipeline {
    agent none
    options {
        skipStagesAfterUnstable()
    }
        stage('Deliver') { 
            agent any
            environment { 
                VOLUME = '$(pwd)/src'
                IMAGE = 'cdrx/pyinstaller-windows:python3'
            }
            steps {
                dir(path: env.BUILD_ID) {
                    sh "docker run --rm -v ${VOLUME} ${IMAGE} 'pyinstaller -F main.py --noconsole --onefile --icon=PurlsIcon.ico --name SWLUUpdater'"
                }
            }
            post {
                success {
                    archiveArtifacts "${env.BUILD_ID}/dist/SWLUUpdater.exe"
                    sh "docker run --rm -v ${VOLUME} ${IMAGE} 'rm -rf build dist'"
                }
            }
        }
    }
}