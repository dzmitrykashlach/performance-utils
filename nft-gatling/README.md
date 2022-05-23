gatling-maven-plugin-poc
=========================

Simple showcase of a maven project using the gatling-maven-plugin.

To test it out, simply execute the following command:

    $mvn gatling:test -Dgatling.simulationClass=enwiki.StagSimulation  

For logging in to ENWIKI Stag environment through impersonation `credentials.conf` should be put to `src\test\resources\`  

Format:

`credentials {
username = ""
password = ""
}`

Only user, configured in impersonation plugin is allowed to log in.
